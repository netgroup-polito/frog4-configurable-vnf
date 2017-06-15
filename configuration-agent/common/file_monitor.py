import pyinotify

class FileMonitor(pyinotify.ProcessEvent):

    def initialize(self, file_to_monitor_path, event_type, callback_function):
        self.file_to_monitor = file_to_monitor_path
        self.event_type = event_type
        self.callback_function = callback_function

        self.event_type_const = None
        if event_type == "modify":
            self.event_type_const = pyinotify.IN_MODIFY
        elif event_type == "create":
            self.event_type_const = pyinotify.IN_CREATE
        elif event_type == "delete":
            self.event_type_const = pyinotify.IN_DELETE
        print(self.event_type_const)

    def start_monitoring(self):
        wm = pyinotify.WatchManager()
        notifier = pyinotify.Notifier(wm)
        # In this case you must give the class object (ProcessTransientFile)
        # as last parameter not a class instance.
        wm.watch_transient_file(self.file_to_monitor, self.event_type_const, FileMonitor)
        notifier.loop()


    def process_IN_MODIFY(self, event):
        # We have explicitely registered for this kind of event.
        print(event.pathname + ' -> modified')

    def process_IN_CREATE(self, event):
        # We have explicitely registered for this kind of event.
        print(event.pathname + ' -> created')

    def process_IN_DELETE(self, event):
        # We have explicitely registered for this kind of event.
        print(event.pathname + ' -> deleted')

    def process_default(self, event):
        # Implicitely IN_CREATE and IN_DELETE are watched too. You can
        # ignore them and provide an empty process_default or you can
        # process them, either with process_default or their dedicated
        # method (process_IN_CREATE, process_IN_DELETE) which would
        # override process_default.
        print('default: ' + event.maskname)


