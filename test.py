from eventbus import EventBus
from twisted.internet import task, reactor, threads
import time
import sys
import json

class Tester(object):
  """
  Use this class to flood your vertx sockjs server with websocket connections
  """
  def __init__(self, host, address, max_conn):
    self.interval = 0.01
    self.host = host
    self.address = address
    self.max_conn = max_conn
    self.conns = []
    self.lc = task.LoopingCall(self.new_conn)
    self.lc.start(self.interval)

  def new_conn(self):
    if len(self.conns) <= self.max_conn:
      eb = EventBus("http://{}/eventbus".format(self.host))
      self.conns.append(eb)
      def onopen(message):
        print "onopen"
        eb.registerHandler(self.address, handler)

      def handler(message, replyTo):
        print(message)

      eb.addEventListener("open", onopen)
      threads.deferToThread(eb.connect)

if __name__ == "__main__":
  with open("config.json") as f:
    conf = json.load(f)
    host = conf["host"]
    address = conf["address"].encode("utf8")
    max_conn = conf["socks"]
    tester = Tester(host, address, max_conn)
  reactor.run()
