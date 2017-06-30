from nat.model.nat_session import NatSession

class NatTableParser():

    def parse_nat_table(self, json_nat_table):
        return json_nat_table['nat-session']

    def parse_nat_session(self, json_nat_session_params):

        protocol = None
        if 'protocol' in json_nat_session_params:
            protocol = json_nat_session_params['protocol']

        src_address = None
        if 'src_address' in json_nat_session_params:
            src_address = json_nat_session_params['src_address']

        src_port = None
        if 'src_port' in json_nat_session_params:
            src_port = json_nat_session_params['src_port']

        dst_address = None
        if 'dst_address' in json_nat_session_params:
            dst_address = json_nat_session_params['dst_address']

        dst_port = None
        if 'dst_port' in json_nat_session_params:
            dst_port = json_nat_session_params['dst_port']

        translated_address = None
        if 'translated_address' in json_nat_session_params:
            translated_address = json_nat_session_params['translated_address']

        translated_port = None
        if 'translated_port' in json_nat_session_params:
            translated_port = json_nat_session_params['translated_port']

        tcp_state = None
        if 'tcp_state' in json_nat_session_params:
            tcp_state = json_nat_session_params['tcp_state']

        return NatSession(id=None,
                          protocol=protocol,
                          src_address=src_address,
                          src_port=src_port,
                          dst_address=dst_address,
                          dst_port=dst_port,
                          translated_address=translated_address,
                          translated_port=translated_port,
                          tcp_state=tcp_state
                        )

    def get_nat_session_dict(self, nat_session):

        nat_session_dict = {}

        if nat_session.id is not None:
            nat_session_dict['ip'] = nat_session.id

        if nat_session.protocol is not None:
            nat_session_dict['protocol'] = nat_session.protocol

        if nat_session.src_address is not None:
            nat_session_dict['src_address'] = nat_session.src_address

        if nat_session.src_port is not None:
            nat_session_dict['src_port'] = nat_session.src_port

        if nat_session.src_address is not None:
            nat_session_dict['src_address'] = nat_session.src_address

        if nat_session.dst_address is not None:
            nat_session_dict['dst_address'] = nat_session.dst_address

        if nat_session.dst_port is not None:
            nat_session_dict['dst_port'] = nat_session.dst_port

        if nat_session.translated_address is not None:
            nat_session_dict['translated_address'] = nat_session.translated_address

        if nat_session.translated_port is not None:
            nat_session_dict['translated_port'] = nat_session.translated_port

        if nat_session.tcp_state is not None:
            nat_session_dict['tcp_state'] = nat_session.tcp_state

        return nat_session_dict