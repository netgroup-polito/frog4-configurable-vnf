from message_bus import MessageBus

import logging
import time

class DoubleDeckerDhcpController():

    def __init__(self, message_bus):
        self.messageBus = message_bus
        self.messageBus.set_controller(self)


    def start(self):
        logging.debug("ddDhcpController started")
        while True:
            # Export the status every 3 seconds
            time.sleep(3)
            logging.debug("I'm: ddDhcpController")
        thread.join()


    def on_data_callback(self, src, msg):
        logging.debug("[ddDhcpController] From: " + src + " Msg: " + msg)





