from builtins import str

try:
    import zmq.green as zmq
except ImportError:
    zmq = None

import vaping
import vaping.plugins


@vaping.plugin.register('zeromq')
class ZeroMQ(vaping.plugins.EmitBase):

    def init(self):
        self.log.debug("init zeromq ..")
        if not zmq:
            self.log.error("missing zeromq, please install pyzmq to use this plugin")
            self.skip = True
            return

        self.skip = False

        self.ctx = zmq.Context()
        self.sock = self.ctx.socket(zmq.PUB)
        if 'bind' in self.config:
            self.sock.bind(self.config['bind'])
        else:
            self.log.warning("skipping zeromq, missing config")
            self.skip = True


# TODO option topic
#        self.topic = 'vaping.fping'

    def emit(self, data):
        if self.skip:
            return

# TODO option topic
#        self.sock.send_multipart([self.topic, data])
        self.sock.send_json(data)
        self.log.debug("msg" + str(data))
        self.log.debug("[0MQ] sync send")

