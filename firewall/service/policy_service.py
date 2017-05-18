from firewall.model.policy import Policy
from utils import Bash

import iptc
import logging

class PolicyService():

    def add_policy(self, policy, table, chain):
        if(policy.in_interface is not None or policy.out_interface is not None):
            self._add_policy_in_ebtables(policy, table, chain)
        else:
            self._add_policy_in_iptables(policy, table, chain)

    def remove_policy(self, policy, table, chain):
        if (policy.in_interface is not None or policy.out_interface is not None):
            self._remove_policy_from_ebtables(policy, table, chain)
        else:
            self._remove_policy_from_iptables(policy, table, chain)

    def get_policies(self, table, chain):
        policies = []
        policies.extend(self._get_policies_from_iptables(table, chain))
        policies.extend(self._get_policies_from_ebtables(table, chain))
        return policies

    def get_policy(self, id, table, chain):
        policies = self.get_policies()
        for policy in policies:
            if policy.id == id:
                return policy
        return None



    # private functions

    def _add_policy_in_iptables(self, policy, table, chain):
        # table: FILTER | NAT
        # chain: INPUT | FORWARD | OUTPUT

        table_name = table.upper()
        chain_name = chain.upper()

        rule = iptc.Rule()

        if(policy.src_address is not None):
            rule.src = policy.src_address

        if(policy.dst_address is not None):
            rule.dst = policy.dst_address

        if(policy.protocol != "all"):
            rule.protocol = policy.protocol
            match = rule.create_match(policy.protocol)

        if(policy.src_port is not None):
            match.sport = policy.src_port

        if(policy.dst_port is not None):
            match.dport = policy.dst_port

        if(policy.description is not None):
            match = rule.create_match("comment")
            match.comment = policy.description

        rule.target = iptc.Target(rule, policy.action.upper())

        if table_name == "FILTER":
            table = iptc.Table(iptc.Table.FILTER)
        elif table_name == "NAT":
            table = iptc.Table(iptc.Table.NAT)

        chain = iptc.Chain(table, chain_name)
        chain.insert_rule(rule)

    def _add_policy_in_ebtables(self, policy,  table, chain):
        # table: FILTER | NAT
        # chain: INPUT | FORWARD | OUTPUT

        table_name = table.upper()
        chain_name = chain.upper() + " "

        protocols = []
        if policy.protocol != "all":
            if policy.protocol == "ipv4":
                protocols.append("-p IPv4 ")
            else:
                protocols.append("-p ip --ip-proto " + str(policy.protocol) + " ")
        else:
            protocols.append("-p ip --ip-proto tcp ")
            protocols.append("-p ip --ip-proto udp ")
            protocols.append("-p ip --ip-proto icmp ")

        action = policy.action.upper()

        in_interface = ""
        if(policy.in_interface is not None):
            in_interface = "--in-interface " + str(policy.in_interface) + " "

        out_interface = ""
        if(policy.out_interface is not None):
            out_interface = "--out-interface " + str(policy.out_interface) + " "

        src_address = ""
        if(policy.src_address is not None):
            src_address = "--ip-src " + str(policy.src_address) + " "

        dst_address = ""
        if(policy.dst_address is not None):
            dst_address = "--ip-dst " + str(policy.dst_address) + " "

        src_port = ""
        if (policy.src_port is not None):
            src_port = "--ip-source-port " + str(policy.src_port) + " "

        dst_port = ""
        if (policy.dst_port is not None):
            dst_port = "--ip-destination-port " + str(policy.dst_port) + " "

        for protocol in protocols:
            Bash(
                'ebtables -I ' + chain_name + protocol + in_interface + src_address + src_port + out_interface + dst_address + dst_port + '-j ' + action)

    def _remove_policy_from_iptables(self, policy, table, chain):
        pass

    def _remove_policy_from_ebtables(self, policy, table, chain):
        pass

    def _get_policies_from_iptables(self, table, chain):
        # table: FILTER | NAT
        # chain: ALL | INPUT | FORWARD | OUTPUT

        chain_name = chain.upper()

        table_name = table.upper()
        if table_name == "FILTER":
            table = iptc.Table(iptc.Table.FILTER)
        elif table_name == "NAT":
            table = iptc.Table(iptc.Table.NAT)

        logging.debug("table_name: " + table_name)
        logging.debug("chain_name: " + chain_name)

        policies = []
        table.refresh()
        for chain in table.chains:
            logging.debug("scan chain: " + chain.name + "...")
            if chain.name != chain_name:
                if chain_name != "ALL":
                    continue

            for rule in chain.rules:

                description = None

                for match in rule.matches:
                    if match.name != "comment":
                        description = match.comment

                    src_port = None
                    if match.sport is not None:
                        src_port = match.sport

                    dst_port = None
                    if match.dport is not None:
                        dst_port = match.dport

                in_interface = None
                if rule.in_interface is not None:
                    in_interface = rule.in_interface

                out_interface = None
                if rule.out_interface is not None:
                    out_interface = rule.out_interface

                src_address = None
                if rule.src != "0.0.0.0/0.0.0.0":
                    tmp = rule.src.split('/')
                    src_address = tmp[0]
                    #dict['source-mask'] = tmp[1]

                dst_address = None
                if (rule.dst != "0.0.0.0/0.0.0.0"):
                    tmp = rule.dst.split('/')
                    dst_address = tmp[0]
                    #dict['destination-mask'] = tmp[1]

                # rule.protocol returns "ip" instead of "all"
                protocol = "all"
                if (rule.protocol != "ip"):
                    protocol = rule.protocol

                action = rule.target.name

                policy = Policy(id=None,
                                description=description,
                                action=action,
                                protocol=protocol,
                                in_interface=in_interface,
                                out_interface=out_interface,
                                src_address=src_address,
                                dst_address=dst_address,
                                src_port=src_port,
                                dst_port=dst_port
                                )

                policies.append(policy)

        return policies

    def _get_policies_from_ebtables(self, table, chain):
        policies = []
        return policies

        description = None
        action = None
        protocol = None
        in_interface = None
        out_interface = None
        src_address = None
        dst_address = None
        src_port = None
        dst_port = None

        policy = Policy(id=None,
                        description=description,
                        action=action,
                        protocol=protocol,
                        in_interface=in_interface,
                        out_interface=out_interface,
                        src_address=src_address,
                        dst_address=dst_address,
                        src_port=src_port,
                        dst_port=dst_port
                        )
        policies.append(policy)
