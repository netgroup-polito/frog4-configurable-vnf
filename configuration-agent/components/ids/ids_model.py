class Ids:

    def __init__(self,
                 network_to_defend=None,
                 attacks_to_monitor=[]):

        self.network_to_defend = network_to_defend
        self.attacks_to_monitor = attacks_to_monitor

    def __str__(self):
        str = "{"
        if self.network_to_defend is not None:
            str += "'network_to_defend': " + self.network_to_defend + ", "
        if self.attacks_to_monitor is not None:
            str += "'attacks_to_monitor': {"
            for attack in self.attacks_to_monitor:
                str += attack + ", "
            str += "}, "
        str += "}"
        return str
