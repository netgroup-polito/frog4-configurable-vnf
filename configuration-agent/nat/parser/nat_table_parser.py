class NatTableParser():

    def parse_nat_session(self, json_nat_session_params):
        pass

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