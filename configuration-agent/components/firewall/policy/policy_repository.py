from components.firewall.policy.policy_parser import PolicyParser


class PolicyRepository():

    def __init__(self):
        self.db_file_path = "policy_db.txt"

    def clear_repo(self):
        open(self.db_file_path, 'w').close()

    def save_policy(self, policy):
        id = policy.__hash__()
        policy.id = id
        json_policy = PolicyParser().get_policy_dict(policy)
        self._save_parameter(id, json_policy)
        return id

    def get_policy(self, id):
        json_policy = self._get_parameter(id)
        if json_policy is not None:
            policy = PolicyParser().parse_policy(json_policy)
            return policy
        else:
            return None

    def get_policies(self):
        json_policies = self._get_all_parameters()
        policies = []
        for json_policy in json_policies:
            policy = PolicyParser().parse_policy(json_policy)
            policies.append(policy)
        return policies

    def remove_policy(self, id):
        self._remove_parameter(id)


    def _save_parameter(self, name, value):
        try:
            with open(self.db_file_path, 'a') as db_file:
                db_file.write(name + " " + value + "\n")
                #db_file.truncate()
        except Exception as e:
            raise IOError("Error during the writing of file: " + self.db_file_path + "\n" + str(e))

    def _get_parameter(self, name):
        try:
            with open(self.db_file_path, 'r') as db_file:
                lines = db_file.readlines()
                db_file.close()
        except Exception as e:
            raise IOError("Error during the reading of file: " + self.db_file_path + "\n" + str(e))

        for line in lines:
            args = line.strip().split(' ')
            if args[0] == name:
                return args[1]

        return None

    def _remove_parameter(self, name):
        try:
            with open(self.db_file_path, 'r') as db_file:
                lines = db_file.readlines()
                db_file.close()
        except Exception as e:
            raise IOError("Error during the reading of file: " + self.db_file_path + "\n" + str(e))
        try:
            with open(self.db_file_path, 'w') as db_file:
                for line in lines:
                    args = line.strip().split(' ')
                    if args[0] != name:
                        db_file.write(args[0] + " " + args[1] + "\n")
                #db_file.truncate()
        except Exception as e:
            raise IOError("Error during the writing of file: " + self.db_file_path + "\n" + str(e))


    def _get_all_parameters(self):
        try:
            with open(self.db_file_path, 'r') as db_file:
                lines = db_file.readlines()
                db_file.close()
        except Exception as e:
            raise IOError("Error during the reading of file: " + self.db_file_path + "\n" + str(e))

        parameters = []
        for line in lines:
            args = line.strip().split(' ')
            parameters.append(args[1])
        return parameters