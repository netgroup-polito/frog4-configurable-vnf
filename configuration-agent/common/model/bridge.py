class Bridge:
    def __init__(self, name=None, iface1=None, iface2=None):
        self.name = name
        self.iface1 = iface1
        self.iface2 = iface2

    def __str__(self):
        str = "{"
        if self.name is not None:
            str += "'name': " + self.name + ", "
        if self.iface1 is not None:
            str += "'iface1': " + self.iface1 + ", "
        if self.iface2 is not None:
            str += "'iface2': " + self.iface2
        str += "}"
        return str

    def __eq__(self, other):
        if self.name != other.name:
            return False
        if self.iface1 != other.iface1:
            return False
        if self.iface2 != other.iface2:
            return False
        return True