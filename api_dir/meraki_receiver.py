#!flask/bin/python
from pprint import pprint
from typing import Dict
from flask import request, Response
from meraki_dashboard_api.api import RequestStatusException
from myapi import MyAPI
from flask_restplus import Resource
from datetime import datetime
from flask import Blueprint
from meraki_dashboard_api import MerakiUrls, MerakiAPI
from outputs import to_log_file, to_firehose
from utils import epoch
from app import get_config

mod = Blueprint("v1_0", __name__, url_prefix='/api/v1.0')

api = MyAPI(mod, version="1.0")
config = get_config()


def get_meraki_api() -> MerakiAPI:
    return MerakiAPI(api_key=config.MERAKI_API_KEY)


def get_client_owner(client_mac) -> Dict:
    # todo: can setup a cache here as an optimization
    try:
        device_owner = get_meraki_api().get(MerakiUrls.Networks.client_owner(config.MERAKI_NETWORK_ID, client_mac=client_mac))
    except RequestStatusException as e:
        if e.status_code == 404:
            device_owner = None
        else:
            raise e
    return device_owner


def save_data(data):
    observations = data["observations"]
    now_epoch = epoch(datetime.utcnow())
    out = []
    for i in observations:
        # NOTE: getting the user does not have to happen here (as the total response time for the json post should be < 500ms)
        # It could be off loaded to do a daily batch. This will be something like "user" below will be the email address, id, username, etc... of the device, or None
        device_owner = get_client_owner(i["clientMac"])
        user = device_owner["user"] if device_owner else None
        location = i.get("location")
        out.append({
            "ap": data["apMac"],
            "client_mac": i["clientMac"],
            "lat": location.get("lat") if location else None,
            "lng": location.get("lng") if location else None,
            "identity": user,
            "time_present": i["seenEpoch"],
            "time_now": now_epoch
        })

    # printing here - can send to api, log file, etc...
    # to_log_file(out)
    # to_firehose(out)
    pprint(out)


@api.route('/')
class MerakiBase(Resource):
    def get(self):
        print("validator sent to: ", request.environ['REMOTE_ADDR'])

        return Response(config.MERAKI_VALIDATOR, 200)

    def post(self):
        if not request.json or not 'data' in request.json:
            return "invalid data", 400
        data = request.json
        print("Received POST from ", request.environ['REMOTE_ADDR'])

        # Verify secret
        if data['secret'] != config.MERAKI_SECRET:
            print("secret invalid:", data['secret'])
            return "invalid secret", 403

        # Verify version
        if data['version'] != "2.0":
            print("invalid version")
            return "invalid version", 401

        # Determine device type
        if data['type'] == "DevicesSeen":
            print("WiFi Devices Seen")
        elif data['type'] == "BluetoothDevicesSeen":
            return "Received - Not doing Bluetooth"
        else:
            print("Unknown Device 'type'")
            return ("invalid device type", 403)

        # Do something with data
        save_data(data["data"])

        # Return success message
        return "POST Received"


@api.route('/orgs/')
class Orgs(Resource):
    def get(self):
        orgs = get_meraki_api().get(MerakiUrls.Organizations.organizations())
        return orgs, 200


@api.route('/orgs/<org_id>/networks/')
class OrgNetworks(Resource):
    def get(self, org_id):
        orgs = get_meraki_api().get(MerakiUrls.Organizations.organization_networks(org_id))
        return orgs, 200

