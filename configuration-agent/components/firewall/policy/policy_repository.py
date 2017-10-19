from components.firewall.policy.policy_parser import PolicyParser
import json
import logging
import datetime

# set log level
log_format = '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s %(message)s'
log_date_format = '[%d-%m-%Y %H:%M:%S]'
logging.basicConfig(filename="logging_agent.log", level=logging.DEBUG, format=log_format, datefmt=log_date_format)

class PolicyRepository():

    def __init__(self):
        self.db_file_path = "policy_db.txt"

    def clear_repo(self):
        open(self.db_file_path, 'w').close()

    def save_policy(self, policy):
        id = str(policy.__hash__())
        policy.id = id
        policy_dict = PolicyParser().get_policy_dict(policy)
        self._save_parameter(id, policy_dict)
        #logging.debug("saved policy on repo: " + policy.__str__())
        return id

    def get_policy(self, id):
        json_policy = self._get_parameter(str(id))
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
        self._remove_parameter(str(id))


    def _save_parameter(self, name, value):
        try:
            with open(self.db_file_path, 'a') as db_file:
                now = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
                db_file.write(now + "#" + str(name) + "#" + json.dumps(value) + "\n")
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
            args = line.strip().split('#')
            if args[1].__eq__(name):
                return json.loads(args[2])

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
                    args = line.strip().split('#')
                    if not args[1].__eq__(name):
                        db_file.write(args[0] + "#" + args[1] + "#" + args[2] + "\n")
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
            args = line.strip().split('#')
            param = json.loads(args[2])
            parameters.append(param)
        return parameters