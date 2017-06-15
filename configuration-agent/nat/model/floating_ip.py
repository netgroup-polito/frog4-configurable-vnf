class FloatingIp:

    def __init__(self, private_address=None, public_address=None):
        self.private_address = private_address
        self.public_address = public_address

    def __str__(self):
        str = "{"
        if self.private_address is not None:
            str += "'private_address': " + self.private_address + ", "
        if self.public_address is not None:
            str += "'public_address': " + self.public_address
        str += "}"
        return str

    def __eq__(self, other):
        if self.private_address != other.private_address:
            return False
        if self.public_address != other.public_address:
            return False
        return True