

class MerakiUrls(object):
    class Organizations(object):
        base = "organizations"
        @classmethod
        def organizations(cls, organization_id=None):
            if organization_id:
                return f"{cls.base}/{organization_id}"
            return f"{cls.base}/"

        @classmethod
        def organization_networks(cls, organization_id):
            return f"{cls.base}/{organization_id}/networks"

    class Networks(object):
        base = "networks"

        @classmethod
        def client_owner(cls, network_id, client_mac):
            return f"{cls.base}/{network_id}/clients/{client_mac}"


