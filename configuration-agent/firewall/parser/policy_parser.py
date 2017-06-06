from firewall.model.policy import Policy

import logging

class PolicyParser():

    # it receives the json block that describe the policies
    # and returns an array of policy objects
    def parse_policies(self, json_policies):
        policies = []
        for json_policy in json_policies:
            policy = self.parse_policy(json_policy)
            policies.append(policy)

        return policies

    def parse_policy(self, json_policy):

        description = None
        if 'description' in json_policy:
            description = self.parse_description(json_policy)

        action = None
        if 'action' in json_policy:
            action = self.parse_action(json_policy)

        protocol = None
        if 'protocol' in json_policy:
            protocol = self.parse_protocol(json_policy)

        in_interface = None
        if 'in_interface' in json_policy:
            in_interface = self.parse_in_interface(json_policy)

        out_interface = None
        if 'out_interface' in json_policy:
            out_interface = self.parse_out_interface(json_policy)

        src_address = None
        if 'src_address' in json_policy:
            src_address = self.parse_src_address(json_policy)

        dst_address = None
        if 'dst_address' in json_policy:
            dst_address = self.parse_dst_address(json_policy)

        src_port = None
        if 'src_port' in json_policy:
            src_port = self.parse_src_port(json_policy)

        dst_port = None
        if 'dst_port' in json_policy:
            dst_port = self.parse_dst_port(json_policy)


        return Policy(id=None,
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

    def parse_description(self, json_policy):
        return json_policy['description']

    def parse_action(self, json_policy):
        return json_policy['action']

    def parse_protocol(self, json_policy):
        return json_policy['protocol']

    def parse_in_interface(self, json_policy):
        return json_policy['in-interface']

    def parse_out_interface(self, json_policy):
        return json_policy['out-interface']

    def parse_src_address(self, json_policy):
        return json_policy['src_address']

    def parse_dst_address(self, json_policy):
        return json_policy['dst_address']

    def parse_src_port(self, json_policy):
        return json_policy['src-port']

    def parse_dst_port(self, json_policy):
        return json_policy['dst-port']


    # Give a policy it returns a dictionary
    def get_policy_dict(self, policy):
        policy_dict = {}

        policy_dict['id'] = policy.id

        if policy.description is not None:
            policy_dict['description'] = policy.description

        if policy.action is not None:
            policy_dict['action'] = policy.action

        if policy.protocol is not None:
            policy_dict['protocol'] = policy.protocol

        if policy.in_interface is not None:
            policy_dict['in_interface'] = policy.in_interface

        if policy.out_interface is not None:
            policy_dict['out_interface'] = policy.out_interface

        if policy.src_address is not None:
            policy_dict['src_address'] = policy.src_address

        if policy.dst_address is not None:
            policy_dict['dst_address'] = policy.dst_address

        if policy.src_port is not None:
            policy_dict['src_port'] = policy.src_port

        if policy.dst_port is not None:
            policy_dict['dst_port'] = policy.dst_port

        return policy_dict



