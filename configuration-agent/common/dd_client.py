from doubledecker import clientSafe
from threading import Thread, Lock
import logging

class DDclient(clientSafe.ClientSafe):

    def __init__(self, controller):
        self.controller = controller
        #self.lock = Lock()

    #####################################################
    ################## Public functions #################
    #####################################################

    def set_controller(self, controller):
        self.controller = controller

    def register_to_bus(self, name, dealer_url, customer, keyfile):
        super().__init__(name=name.encode('utf8'),
                         dealerurl=dealer_url,
                         customer=customer.encode('utf8'),
                         keyfile=keyfile)
        thread = Thread(target=self.start)
        thread.start()
        return thread

    def subscribe(self, topic, scope):
        super().subscribe(topic, scope)

    def unsubscribe(self):
        pass

    def publish_public_topic(self, topic, msg):
        #self.lock.acquire()  # will block if lock is already held
        #logging.debug("publish_public_topic: " + topic + " " + msg)
        self.publish_public("public."+topic, msg)
        #self.lock.release()

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
        pass

    def on_data(self, src, msg):
        """ callback for point to point messages """
        src = src.decode()
        msg = msg.decode()
        #logging.debug("[DDClient] From: " + src + " Msg: " + msg)
        self.controller.on_data_callback(src, msg)

    def on_reg(self):
        #logging.debug("[DDclient] on_reg ack")
        self.controller.on_reg_callback()

    def on_error(self, code, msg):
        logging.debug(str(code) + ": " + str(msg))

    def on_discon(self):
        """ callback at disconnection """
        super().on_discon()