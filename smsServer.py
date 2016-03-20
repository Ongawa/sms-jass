#!/usr/bin/env python
# SMS manager

#  y Cambiar reservorios por JASS
#  y Leyenda de graficos, incluir nro de reportes tx
#  y programar fechas de envio de recordatorios
#  n verificar exportar excel
#  n En la hoja resumen, mostrar por reserorio y mostrar por mes 



import time
import serial
import thread
import psycopg2

print "Esperando al Modem.."
for i in range(10,0,-1):
	time.sleep(1)
	print i

DB_NAME='db_sms'
DB_HOST='127.0.0.1'
DB_USER='smsuser'
DB_PASSWORD='secretpwd'

conn = psycopg2.connect(dbname=DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
conn.autocommit = True
cur = conn.cursor()

class gsmModem:
	dev = '/dev/ttyUSB2'
	port = serial.Serial(dev, baudrate=9600, timeout=3.0)
	busy = True
	response = ''
	sresponse = ''
	timeout = 0

	onceaDay = False
	time2Send = '07:00:00'					# Time to send SMS
	days2Send = [4,6,8,10,12,14,16]		# Days to send remenber SMS
	sms2Send  = 3							# Maximun SMS to remenber to take measurement

	def sendCommand(self,command,response,timeout):
		self.response = ''
		self.sresponse = response
		self.port.write(command)
		print "Send:",command
		counter = 0
		while timeout > counter:
			time.sleep(0.1)
			counter = counter + 0.1
			if self.response.find(response) != -1:
				return True
		return False

	def getCommand(self):
		while True:
			if self.sresponse == '>':
				self.response = self.port.read(1)
				self.sresponse = ''
			else:
				self.response = self.port.readline()
			if len(self.response) > 0:
				print "Received:",repr(self.response)
			if self.response.find('+CMTI')!=-1:
				self.port.write('AT+CMGL="ALL"\r')
			if self.response.find('+CMGL')!=-1:
				self.busy = True
				response = self.response
				totalresponse = response
				while response != 'OK\r\n':
					response = self.port.readline()
					totalresponse = totalresponse+response

				messages = totalresponse.split("+CMGL")
				for i in messages:
					if len(i)>0:
						contends = i.split('\r\n')
						contends_info = contends[0].split(',')
						contends_data=''
						for i in contends[1:]:
							contends_data = contends_data+i
						if contends_data[-2:]=="OK":
							contends_data = contends_data[:-2]

						if contends_info[2].find('+51') != -1:
							info_number   = contends_info[2].replace('"','').replace('+51','')
							info_datetime = contends_info[4]+","+contends_info[5]
							info_date = ('20'+info_datetime.split(",")[0][1:]).replace('/','-')
							info_time = info_datetime.split(",")[1][:-4]

							self.readSMS(info_number,info_date,info_time,contends_data)
						
				self.sendCommand('AT+CMGD=,3\r','OK\r',10)
				self.busy=False	

	def init(self):
		self.busy = True
		while True:
			if self.sendCommand('AT\r','OK\r',10):
				self.sendCommand('ATE0\r','OK\r',10)
				time.sleep(2)
				self.sendCommand('AT+CPMS="SM","SM","SM"\r','OK\r',10)
				time.sleep(2)
				self.sendCommand('AT^CURC=0\r','OK\r',10)
				time.sleep(2)
				self.sendCommand('AT+CMEE=2\r','OK\r',10)
				time.sleep(2)
				self.sendCommand('AT+CMGF=1\r','OK\r',10)
				time.sleep(2)
				self.sendCommand('AT+CNMI=1,1,0,1,0\r','OK\r',10)
				time.sleep(2)
				break
			else:
				print "...Turning Module ON"
				time.sleep(2)
				time.sleep(5)
		self.busy = False

	def sendSMS(self,message, number):
		self.sendCommand('AT+CMGS="%s"\r'%number,'>',10)
		return self.sendCommand("%s%s"%(message,chr(26)),'OK\r',10)


	def getMeasurement(self,message):
			#Allowed Formats 
			#1.-CLORO SI, MEDICION 0 .5, CAUDAL 1.0, PAGOS 25  
			#2.-cloro si, medicion 0.5, caudal 1.0, pagos 25 
			#3.-cloro SI, m 0.5, c 1. 0, p 25 
			#4.-cloro si, 0.5,1.0,25
			#5.-si, 0.5    ,1.0,  25
		message = message.lower()
		parts = message.split(',')
		if len(parts) == 4:
			messageData = message[:message.index(',')]
			if messageData.find('si')!=-1:
				measurement = '1'
			elif messageData.find('no')!=-1:
				measurement = '0'
			else:
				measurement=''
			messageData = message[message.index(','):]
			measurement =  self.getNumbers(measurement,messageData)
			parts = measurement.split(',')
			for i in parts:
				try:
					float(i)
				except:
					return False
			return measurement
		else:
			return False

	def getNumbers(self,measurement, messageData):
		for i in messageData:
			if i.isdigit() or (i == '.') or (i == ','):
				measurement = measurement + i
		return measurement

	def getCut(self,message):
			#Allowed Formats 
			#1.-corte reparacion 12
			#2.-corte man 1 
			#3.-corte mantenimiento 1 
			#4.-corte reparacion 1
		message = message.lower()
		if message.find('corte')!= -1:
			if message.find('man') != -1:
				reason = 'Mantenimiento'
			elif message.find('rep') != -1:
				reason = 'Reparacion'
			else:
				return False
			measurement = ''
			measurement = self.getNumbers(measurement,message)
			
			if measurement == '':
				return False
			else:
				return "%s,%s"%(reason,measurement)

		else:
			return False

	def monthsBefore(self,m):
		current = time.localtime()
		currentY = current[0]
		currentM = current[1]
		y = m/12
		m = m%12
		mb = currentM-m
		yb = currentY-y
		if mb<=0:
			mb = mb+12
			yb = yb -1
		return '%04d-%02d'%(yb,mb)

	def readSMS(self,number,date,tim,message):
		processed = False
		try:
			c_search1 = """
					SELECT reservoir_id FROM "public"."Data_reservoir_manager_id"
					WHERE manager_id = '%s';
					"""%str(number)
			cur.execute(c_search1)
			searchResult = cur.fetchall()
			reservoir = searchResult[0][0]
			c_search2 = """
					SELECT number_user FROM "public"."Data_reservoir"
					WHERE reservoir_id = '%s';
					"""%str(reservoir)
			cur.execute(c_search2)
			searchResult = cur.fetchall()
			users = searchResult[0][0]
		
		except:
			reservoir = 'Desconocido'
		print reservoir

		cut = self.getCut(message)
		measurement = self.getMeasurement(message)
		if measurement:
			#1.-CLORO SI, MEDICION 0 .5, CAUDAL 1.0, PAGOS 25  
			data     = measurement.split(',')
			add_cl   = data[0]
			level_cl = data[1]
			caudal   = data[2]
			user_pay = data[3]
			c_insert = """
				UPDATE "public"."Data_measurement"
				SET
					date ='%s',
					time ='%s',
					level_cl ='%s',
					add_cl ='%s',
					caudal ='%s',
					user_pay ='%s/%s'
				WHERE reservoir_id_id = '%s' and date::text LIKE '%s';
				"""%(date,tim,level_cl,add_cl,caudal,user_pay,users,reservoir,self.monthsBefore(0)+'%')
			cur.execute(c_insert)
			processed = True

		if cut:
			data     = cut.split(',')
			reason	 = data[0]
			duration = data[1]
			c_insert = """
				INSERT INTO "public"."Data_interruption"(date,time,reason,duration,reservoir_id_id) 
				VALUES ('%s','%s','%s','%s','%s');
				"""%(date,tim,reason,duration,reservoir)
			cur.execute(c_insert)
			processed = True
		
		if processed:
			feedbackmessage = 'Gracias, la informacion enviada ha sido procesada correctamente.'
		else:
			feedbackmessage = 'Error en el envio. Por Favor, revise el formato de SMS e intentelo nuevamente.'

		c_insert ="""
			INSERT INTO "public"."Data_outbox"(outbox_id,message,date,time) 
			VALUES ('%s','%s','%s','%s');
			""" %(number,feedbackmessage,date,tim) 
		cur.execute(c_insert)

		c_insert = """
			INSERT INTO "public"."Data_record"(date,time,message,detail,process,reservoir_id) 
			VALUES ('%s','%s','%s@%s','%s','%s','%s');
			"""%(date,tim,message,number,'Entrada',processed,reservoir)
		cur.execute(c_insert)

	def completeData(self):
	# check for reservoirs
		c_search = """
		SELECT reservoir_id, number_user FROM "public"."Data_reservoir";
		"""
		cur.execute(c_search)
		reservoirs = cur.fetchall()
	# see if there are at least n months on the table
		for r in reservoirs:
			n = 6
			for i in range(n):
				#see if there are data for selected month
				c_search = """
				SELECT * FROM "public"."Data_measurement"
				WHERE date::text LIKE  '%s' and reservoir_id_id = '%s';
				"""%(self.monthsBefore(i)+'%',r[0])
				cur.execute(c_search)
				reservoir = cur.fetchall()
				if len(reservoir) == 0:
					c_insert ="""
					INSERT INTO "public"."Data_measurement"(date,time,level_cl,add_cl,caudal,user_pay,reservoir_id_id) 
								VALUES ('%s','00:00:00','0','0','0','0/%s','%s');
					""" %(self.monthsBefore(i)+'-01',r[1],r[0]) 
					cur.execute(c_insert)

		for r in reservoirs:
			c_search = """
			SELECT * FROM "public"."Data_measurement"
			WHERE date::text LIKE  '%s' and reservoir_id_id = '%s';
			"""%(self.monthsBefore(0)+'%',r[0])
			cur.execute(c_search)
			reservoir = cur.fetchall()[0]
			data = '%s%s%s%s'%(reservoir[2],reservoir[3],reservoir[4],reservoir[5])
			if data == '00:00:00000':
				try:
					c_insert="""
					INSERT INTO "public"."Data_remenber"(remenber_id,sent) 
					VALUES ('%s','1');
					""" %r[0]
					cur.execute(c_insert)
				except:
					pass
			else:
				c_delete="""
				DELETE FROM "public"."Data_remenber" 
				WHERE remenber_id = '%s';
				""" %r[0]
				cur.execute(c_delete)
				c_delete="""
				DELETE FROM "public"."Data_outbox" 
				WHERE outbox_id IN (
					SELECT manager_id_id FROM "public"."Data_reservoir" 
					WHERE reservoir_id = '%s');
				""" %r[0]
				#cur.execute(c_delete)

	def makeRemenber(self):
		if time.localtime()[3] <= 1:
			self.onceaDay = True
		
		if self.onceaDay:
			if time.localtime()[3]>=int(self.time2Send.split(':')[0]):
				print self.onceaDay
				time.sleep(4)
				self.init()
				# look for reservoir and count < to count, send SMS, then add a number to the count
				try:
					c_message = """SELECT message FROM "public"."Data_format_message" LIMIT 1;"""
					cur.execute(c_message)
					messageFormat = cur.fetchall()[0]
				except:
					messageFormat = 'Buenos dias. Envie su reporte de medicion a la brevedad.'
				c_search = """
				SELECT reservoir_id,sent,manager_id_id,name
				FROM "public"."Data_remenber","public"."Data_reservoir","public"."Data_manager"
				WHERE remenber_id = reservoir_id and phone = manager_id_id;"""
				cur.execute(c_search)
				reservoirs = cur.fetchall()
				for r in reservoirs:
					# Test if today its a day2Send
					if time.localtime()[2] in self.days2Send:
						# Test if there are less sms2Send
						if r[1]<=self.sms2Send:
							dateC = time.strftime('%Y-%m-%d',time.localtime())
							timeC = time.strftime('%H:%M:%S',time.localtime())

							c_insert ="""
							INSERT INTO "public"."Data_outbox"(outbox_id,message,date,time) 
							VALUES ('%s','%s, %s - JASS %s','%s','%s');
							""" %(r[2],r[3],messageFormat[0],r[0],dateC,timeC) 
							cur.execute(c_insert)
							
							c_update ="""
							UPDATE "public"."Data_remenber"
							SET sent = '%s'
							WHERE remenber_id = '%s'
							""" %(str(r[1]+1),r[0]) 
							cur.execute(c_update)

				self.onceaDay = False

	def smsSender(self):
		while True:
			if not(self.busy):
				self.completeData()
				self.makeRemenber()
				c_search = 'SELECT outbox_id, message FROM "public"."Data_outbox"'
				cur.execute(c_search)
				mensajesLeft = cur.fetchall()
				if len(mensajesLeft)>0:
					for i in mensajesLeft:
						number = i[0]
						message = i[1]

						if self.sendSMS(message,number):
						#if False:
							c_remove = """
								DELETE FROM "public"."Data_outbox"
								WHERE outbox_id = '%s' and message = '%s';
								"""%(number,message)
							cur.execute(c_remove)
							date = time.strftime('%Y/%m/%d',time.localtime()) 
							tim  = time.strftime('%H:%M:%S',time.localtime())
							direction = "Salida"
							processed = True
							c_search = """
								SELECT reservoir_id FROM "public"."Data_reservoir"
								WHERE manager_id_id = '%s';
								"""%str(number)
							try:
								cur.execute(c_search)
								reservoir = cur.fetchall()[0][0]
							except:
								reservoir = 'Desconocido'

							c_insert = """
								INSERT INTO "public"."Data_record"(date,time,message,detail,reservoir_id,process) 
								VALUES ('%s','%s','%s','%s','%s','%s');
								"""%(date,tim,message+'@'+str(number),direction,reservoir,processed)
							cur.execute(c_insert)
			time.sleep(10)




fona = gsmModem()
thread.start_new_thread(fona.getCommand,())
thread.start_new_thread(fona.smsSender,())

fona.init()
while True:
	time.sleep(10)

