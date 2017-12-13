#!/usr/bin/python
import tornado.ioloop
import tornado.websocket


import threading
import sqlite3
import json
import socket
import time
import math
from datetime import datetime

import snmp
 

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

        	# sqlite3 connections (read)
			conn_r = sqlite3.connect('local.db')
			conn_r.row_factory = sqlite3.Row
			c_r = conn_r.cursor()

			t = (req['time'],)
			c_r.execute('SELECT * FROM monitories WHERE tstamp>? ORDER BY tstamp DESC', t)
			results = c_r.fetchmany(size=20)

			keys = ['tstamp', 'temperature', 'humidity', 'humidex', 'power', 'energy', 'traffic', 'co2', 'co2pbit', 'comfort']
			# unused fields: id

			res = {}
			for k in keys:
				res[k] = [r[k] for r in results]

			# print res
			# print '##'

			# res = {'message': [dict(results[i]) for i in range(0, len(results))]}

			conn_r.close()
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
		# arduino_data = sock.recv(1024)
		arduino_data = '{"t": 20, "h": 20}'
		time.sleep(5)
		# handle receive
		# print "received message:", data

def stop_arduino_udp():
	print 'Stopping Arduino-UDP service...'
	sock.close()

def run_datacapture():
	print 'Starting Data-Capture service...'

	global arduino_data
	# fake
	# arduino_data = {'t': 20, 'h': 20}


	# init
	traffic0 = snmp.get_traffic()
	energy = 0.0

	while True:

		# 1 sec delay
		time.sleep(1)

		# wait for arduino data to be received
		if arduino_data != -1:
			print ' # Capturing data: ' + datetime.now()

			# get arduino data
			sensor_data = json.loads(arduino_data)

			# get SNMP data
			traffic = snmp.get_traffic() - traffic0		# delta-bytes
			power = snmp.get_power()					# W

			# accumulate power
			energy += power / 3600.0

			# 82 CO2-g/KWh
			co2 = energy * 0.082
			co2pbit = co2 / (traffic * 8)

			##################################################################################################		
			# sensor_data['t'] = 
			# sensor_data['h'] = 

			kelvin = sensor_data['t'] + 273;
			eTs = 10 ** ((-2937.4 /kelvin) - 4.9283 * math.log(kelvin) / math.log(10) + 23.5471)
			eTd = eTs * sensor_data['h'] / 100.0;

			humidex = int(round(sensor_data['t'] + ((eTd-10)*5.0/9.0)))
			##################################################################################################

			if humidex < 25:
				comfort = 1
			elif humidex < 34:
				comfort = 2
			elif humidex < 40:
				comfort = 3
			elif humidex < 45:
				comfort = 4
			else:
				comfort = 5

			timestamp = int(round(time.time()))

			# sqlite3 connection (write)
			conn_w = sqlite3.connect('local.db')
			c_w = conn_w.cursor()

			# insert data
			c_w.execute("INSERT INTO monitories (tstamp, temperature, humidity, humidex, power, energy, traffic, co2, co2pbit, comfort) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (timestamp, sensor_data['t'], sensor_data['h'], humidex, power, energy, traffic, co2, co2pbit, comfort))

			# commit the changes
			conn_w.commit()

			conn_w.close()
		else:
			print ' # No sensor data'

def stop_datacapture():
	print 'Stopping Data-Capture service...'

def stop_db():
	print 'Closing database connections...'
	# conn_r.close()
	# conn_w.close()

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
