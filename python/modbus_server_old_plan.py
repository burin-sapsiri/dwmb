import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import time
import json
from minimalmodbus import *

ws_client = []

dev0 = Instrument('/dev/ttyUSB0', 2)

dev_gpio = [0, 0, 0, 0, 0, 0, 0, 0]

def read_gpio(addr, gpio_addr) :
    try :
        dev0.set_addr(addr)
        data = int(dev0.read_register(gpio_addr))
        return data
    except IOError :
        print "Error : " + str(IOError.message)

def write_gpio(addr, gpio_addr, value) :
    try :
        dev0.set_addr(addr)
        dev0.write_register(gpio_addr, value)

    except IOError :
        print "Error : " + str(IOError.message)

#================Tornado Class Handler================
class MainHandler(tornado.web.RequestHandler):
    def get(self):
       self.write("Hello, world") 
       print "There is income connection"

class MBNodeHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        dev_json = json.dumps(dev_gpio)
        self.write_message(dev_json)

        ws_client.append(self)
        print "There is income connection"
    def on_close(self):
        ws_client.remove(self)
        print "The income connection was closed"
    def on_message(self, message):

        in_dev_json = json.loads(message)

        if (in_dev_json[0] == 0) :
            write_gpio(2, 2, in_dev_json[1])
        elif (in_dev_json[0] == 1) :
            write_gpio(2, 3, in_dev_json[1])
        elif (in_dev_json[0] == 2) :
            write_gpio(2, 4, in_dev_json[1])
        elif (in_dev_json[0] == 3) :
            write_gpio(2, 5, in_dev_json[1])
        elif (in_dev_json[0] == 4) :
            write_gpio(3, 2, in_dev_json[1])
        elif (in_dev_json[0] == 5) :
            write_gpio(3, 3, in_dev_json[1])
        elif (in_dev_json[0] == 6) :
            write_gpio(3, 4, in_dev_json[1])
        elif (in_dev_json[0] == 7) :
            write_gpio(3, 5, in_dev_json[1])

        dev_gpio[in_dev_json[0]] = in_dev_json[1]

        dev_json = json.dumps(dev_gpio)
        for i in range(0, len(ws_client)) :
            ws_client[i].write_message(dev_json)

    def write(self, message):
        pass
#=====================================================

def loop_read() :
    dev_json = json.dumps(dev_gpio)

    for i in range(0, len(ws_client)) :
        ws_client[i].write_message(dev_json)

#==================Tornado Initial====================
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/mbnode", MBNodeHandler),
])

if __name__ == "__main__":
    application.listen(8888)

    write_gpio(2, 2, 0)
    write_gpio(2, 3, 0)
    write_gpio(2, 4, 0)
    write_gpio(2, 5, 0)

    write_gpio(3, 2, 0)
    write_gpio(3, 3, 0)
    write_gpio(3, 4, 0)
    write_gpio(3, 5, 0)

    #loop_read_hndl = tornado.ioloop.PeriodicCallback(loop_read, 1000)
    #loop_read_hndl.start()

    main_loop = tornado.ioloop.IOLoop.instance()
    main_loop.start()
#=====================================================
