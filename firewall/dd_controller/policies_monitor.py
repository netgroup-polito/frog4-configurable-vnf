class PoliciesMonitor():

    def __init__(self, dd_controller, curr_interfaces):
        pass

    def start_monitoring(self):
        pass

    def _get_new_policies(self):
        pass

    def _find_diff(self, old_policy, new_policy):
        pass

    def _publish_policy_leafs_on_change(self, id, policy, method):
        pass

    def _publish_policy_leafs_periodic(self, policy, period):
        pass

    def _timer_periodic_callback(self, period):
        pass


    ################### Private publish functions ###################
    def _publish_policy(self, id, data, method=None):
        pass

    def _publish_policy_description(self, id, data, method=None):
        pass

    def _publish_policy_action(self, id, data, method=None):
        pass

    def _publish_policy_protocol(self, id, data, method=None):
        pass

    def _publish_policy_in_interface(self, id, data, method=None):
        pass

    def _publish_policy_out_interface(self, id, data, method=None):
        pass

    def _publish_policy_src_address(self, id, data, method=None):
        pass

    def _publish_policy_dst_address(self, id, data, method=None):
        pass

    def _publish_policy_src_port(self, id, data, method=None):
        pass

    def _publish_policy_dst_port(self, id, data, method=None):
        pass