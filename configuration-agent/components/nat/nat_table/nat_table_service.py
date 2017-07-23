from components.nat.nat_table.nat_session_model import NatSession
import pynetfilter_conntrack
import netifaces

class NatTableService():

    def get_nat_table(self):
        ct = pynetfilter_conntrack.Conntrack()
        nat_table = []
        for item in ct.dump_table(netifaces.AF_INET)[0]:
            nat_session = NatSession(
                id=None,
                protocol=item.orig_l4proto,
                src_address=item.orig_ipv4_src,
                src_port=item.orig_port_src,
                dst_address=item.orig_ipv4_dst,
                dst_port=item.orig_port_dst,
                translated_address=item.repl_ipv4_dst,
                translated_port=item.repl_port_dst,
                tcp_state=item.tcp_state
            )
            # Discard tcp connection not natted
            if not nat_session.src_address.__eq__(nat_session.translated_address):
                nat_table.append(nat_session)
        return nat_table

    def add_nat_session(self, nat_session):
        pass