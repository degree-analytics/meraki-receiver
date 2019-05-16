# Meraki API Location Receiver App


### Overview of Process 
- Flask API Running
- Confirms Secret Keys w/ Meraki to enable Post Forwarding Location API via a GET Request
- Meraki then sends data via POST requests
- App Takes data, manipulates it (grabs user associated with device)
- Then pushes data to some output (console, log file, AWS Firehose)



## Prerequisites
* Python >= 3.6
* Cisco Meraki Network with Location Scanning API enabled and configured to point to this server

## Installation and Run
```
$ git clone <<this repo>>
```
* Install Requirements `pip3 install -r requirements.txt`
* Adjust settings in `settings.py` to reflect your secret keys and such
    * AWS Firehose config is there as well
* Start Flask App - `python application.py`


## Helpful Things...
**Getting Meraki Org & Network ID**

If you are not sure what your Org or Network IDs are, use the provided endpoints:
* `/api/v1.0/orgs/` to get list of Orgs
* '/api/v1.0/orgs/<org_id>/networks/' to get Network ID


**500ms SLA**:
Location API is designed such that your SLA should be under 500ms per request. If complex operations are being done while manipulating the data (like looking up the user), consider kicking off a separate subprocess or send to a different queue to make sure you don't drop any data


**ngrok**

[ngrok](ngrok.com) - very helpful when testing. Helps establish a temporary public url to your local host
```
ngrok http 5000
```

**Overall API Pattern**

Uses an Application Factory Pattern. Essentially, you will find the different modes of running the app in `settings.py`. By default, will run in `LOCAL`. For it to run other settings like `PROD`, set the environmental variable `SERVER_TYPE`

# Cisco Meraki CMX Location API Documentation


To enable the location scanning API, see instructions [here](https://documentation.meraki.com/MR/Monitoring_and_Reporting/Location_Analytics#Enable_Scanning_API) under *Enable Location API* section
### Written by Degree Analytics
GET/POST calls inspired by [Cory Guynn's repo](https://github.com/dexterlabora/cmxreceiver-python)


Copyright (c) 2019 MF Genius, Corp d/b/a Degree Analytics
MIT License

Please let us know if you are using this script or have any questions - support@degreeanalytics.com