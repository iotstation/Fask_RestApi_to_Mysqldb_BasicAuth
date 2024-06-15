from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error 
import traceback
from flask_httpauth import HTTPBasicAuth



app = Flask(__name__)
auth= HTTPBasicAuth()


users ={
	"admin":"12345678",
	"iot":"87654321"
}

@auth.verify_password
def verify_password(username,password):
	if username in users and users[username] == password:
		return username
		
	

def insert_data(temp,hum, username):
	try:
		connection =mysql.connector.connect(
			host = '127.0.0.1',
			port = '3306',
			database= 'your-db-name',
			user='your-db-username',
			password='your-db-password'

			)
		if connection.is_connected():
			cursor=connection.cursor()

			insert_query="""INSERT INTO sensor (temp, hum, username) VALUES(%s, %s , %s);  """

			data= (temp,hum,username)

			cursor.execute(insert_query,data)
			connection.commit()
			print("Data inserted Successfully")

	except Error as e:
		print("MYSQL Error:", e)
		traceback.print_exc()
	finally:
		if connection.is_connected():
			cursor.close()
			connection.close()
			print("MYSQL Conection is closed")
@app.route('/data',methods=['POST'])
@auth.login_required
def recived_data():
	try:
	
		data = request.get_json()
		if data:
			print("Recived data:", data)

			temp = data.get('temp')
			hum = data.get('hum')

			if temp is not None and hum is not None:
				username = auth.current_user()
				insert_data(temp,hum,username)
				return jsonify({"message": "Data Recived", "data": data}), 200
			else:
				return jsonify({"error":"Invalid data format"}), 400
		else:
			return jsonify({"error": "No Data Recived"}),400
			
	except Exception as e:
		print("Error:", e)
		traceback.print_exc()
		return jsonify({"error":"Internal server"}), 500

if __name__=='__main__':
	app.run(host='0.0.0.0', port=5000)

			