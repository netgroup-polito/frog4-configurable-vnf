from doubledecker import clientSafe
from threading import Thread
import logging

class DDclient(clientSafe.ClientSafe):

    def __init__(self, controller):
        self.controller = controller

    #####################################################
    ################## Public functions #################
    #####################################################

    def set_controller(self, controller):
        self.controller = controller

    def register_to_bus(self, name, dealer_url, keyfile):
        super().__init__(name=name.encode('utf8'),
                         dealerurl=dealer_url,
                         keyfile=keyfile)
        thread = Thread(target=self.start)
        thread.start()
        return thread

    def subscribe(self, topic, scope):
        super().subscribe(topic, scope)

    def unsubscribe(self):
        pass

    def publish_public_topic(self, topic, msg):
        #logging.debug("publish_public_topic: " + topic + " " + msg)
        self.publish_public(topic, msg)

    def publish_topic(self, topic, msg):
        #logging.debug("public_topic: " + topic + " " + msg)
        self.publish(topic, msg)

    def send_message(self, dst, msg):
        self.sendmsg(dst, msg)

    #####################################################
    ############## Double Decker callbacks ##############
    #####################################################

    def start(self):
        super().start()

    def on_pub(self, src, topic, msg):
        """ callback for published messages """
        src = src.decode()
        topic = topic.decode()
        msg = msg.decode()
        #logging.debug("(on_pub) From: " + src + " Topic: " + topic + " Msg: " + msg)
        self.controller.on_pub_callback(src, topic, msg)

    def on_data(self, src, msg):
        """ callback for point to point messages """
        src = src.decode()
        msg = msg.decode()
        #logging.debug("(on_data) From: " + src + " Msg: " + msg)
        self.controller.on_data_callback(src, msg)

    def on_reg(self):
        self.controller.on_reg_callback()

    def on_error(self, code, msg):
        logging.debug(str(code) + ": " + str(msg))

    def on_discon(self):
        """ callback at disconnection """
        super().on_discon()