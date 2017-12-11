#!/usr/bin/python
import tornado.ioloop
import tornado.websocket

import sqlite3
import json
 
conn = sqlite3.connect('local.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
 
    def open(self):
        print("WebSocket opened")
 
    def on_message(self, message):

        req = json.loads(message)

        if req['type'] == 'query':
            t = (req['time'],)
            c.execute('SELECT * FROM entries WHERE timestamp>? ORDER BY timestamp DESC', t)
            results = c.fetchmany(size=20)

            keys = ['id', 'timestamp', 'temperature', 'humidity', 'humidex', 'power', 'traffic', 'co2', 'co2pbit', 'comfort']

            res = {}
            for k in keys:
            	res[k] = [r[k] for r in results]

            print res
            print '##'

            # res = {'message': [dict(results[i]) for i in range(0, len(results))]}
            self.write_message(res)

    def on_close(self):
        print("WebSocket closed")

def make_app():
    return tornado.web.Application([
        (r"/websocket", EchoWebSocket),
    ])

def data_in():
	# read arduino

	# read SNMP

	# write to db
	pass

def data_out():
	pass
 
if __name__ == "__main__":
	app = make_app()
	app.listen(9999)
	tornado.ioloop.IOLoop.current().start()