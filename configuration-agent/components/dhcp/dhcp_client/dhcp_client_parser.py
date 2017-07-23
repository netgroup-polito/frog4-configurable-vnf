class DhcpClientParser():

    def get_client_dict(self, client):

        client_dict = {}

        if client.mac_address is not None:
            client_dict['mac_address'] = client.mac_address

        if client.ip_address is not None:
            client_dict['ip_address'] = client.ip_address

        if client.hostname is not None:
            client_dict['hostname'] = client.hostname

        if client.valid_until is not None:
            client_dict['valid_until'] = client.valid_until

        return client_dict