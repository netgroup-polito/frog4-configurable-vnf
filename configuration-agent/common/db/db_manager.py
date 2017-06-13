database = "my_db.txt"

class dbManager():

    def clear_db(self):
        open(database, 'w').close()

    def read_interface_id(self, name_iface):
        rows = self._read_file()
        id = None
        for row in rows:
            name = row.strip().split(' ')[0]
            if name.__eq__(name_iface):
                id = row.strip().split(' ')[1]
                break
        return id

    def write_interface_id(self, id, name):
        try:
            with open(database, 'a') as my_db:
                my_db.write(name+' '+id+'\n')
            my_db.close
        except Exception as e:
            raise IOError("Error during writing of my_db. File: " + database + " \n" + str(e))

    def _read_file(self):
        try:
            with open(database, 'r') as my_db:
                rows = my_db.readlines()
            my_db.close
            return rows
        except Exception as e:
            raise IOError("Error during reading of my_db. File: " + database + " \n" + str(e))
