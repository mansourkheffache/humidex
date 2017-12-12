#!/usr/bin/python
import tornado.ioloop
import tornado.websocket

import threading

import sqlite3
import json
import socket
import time
 

# sqlite3 connections (write)
conn_r = sqlite3.connect('local.db')
conn_r.row_factory = sqlite3.Row
c_r = conn_r.cursor()

# sqlite3 connection (write)
conn_w = sqlite3.connect('local.db')
c_w = conn_w.cursor()

# Tornado WS info
WS_PORT = 9999

# UDP info
UDP_IP = '192.168.5.3'
UDP_PORT = 5005

# globals
arduino_data = -1

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
 
    def open(self):
        print("WebSocket opened")
 
    def on_message(self, message):

        req = json.loads(message)

        if req['type'] == 'query':
            t = (req['time'],)
            c_r.execute('SELECT * FROM entries WHERE timestamp>? ORDER BY timestamp DESC', t)
            results = c_r.fetchmany(size=20)

            keys = ['timestamp', 'temperature', 'humidity', 'humidex', 'power', 'traffic', 'co2', 'co2pbit', 'comfort']
            # unused fields: id

            res = {}
            for k in keys:
            	res[k] = [r[k] for r in results]

            # print res
            # print '##'

            # res = {'message': [dict(results[i]) for i in range(0, len(results))]}
            self.write_message(res)

    def on_close(self):
        print("WebSocket closed")
 
def run_tornado():
	print 'Starting Tornado service...'
	app =  tornado.web.Application([(r"/websocket", EchoWebSocket),])
	app.listen(WS_PORT)
	tornado.ioloop.IOLoop.current().start()

def stop_tornado():
	print 'Stopping Tornado service...'
	tornado.ioloop.IOLoop.current().stop()

def run_arduino_udp():
	print 'Starting Arduino-UDP service...'
	sock.bind((UDP_IP, UDP_PORT))

	while True:
		global arduino_data
		arduino_data = sock.recv(1024)
		# handle receive
		# print "received message:", data

def stop_arduino_udp():
	print 'Stopping Arduino-UDP service...'
	sock.close()

def run_datacapture():
	print 'Starting Data-Capture service...'

	global arduino_data
	while True:
		# get arduino data
		# get SNMP data
		# format database record
		# insert
		# bye

		time.sleep(1)
		print arduino_data

def stop_datacapture():
	print 'Stopping Data-Capture service...'

def stop_db():
	print 'Closing database connections...'
	conn_r.close()
	conn_w.close()

if __name__ == "__main__":

	# start threads
	for target in (run_tornado, run_arduino_udp, run_datacapture):
		thread = threading.Thread(target=target)
		thread.daemon = True
		thread.start()

	print '## Services running - Ctrl+C to stop'

	# idle until shutdown signal
	try:
		while True:
			raw_input('')
	except KeyboardInterrupt:
		print 'Stopping all services...'
		stop_tornado()
		stop_arduino_udp()
		stop_datacapture()
		stop_db()
		exit(0)
