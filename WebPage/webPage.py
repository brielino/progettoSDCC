import json
import time
import boto3
from boto3.resources import response
from flask import Flask, render_template, request
from Cloud import GoogleL, ConnectionDB
patients = []
application = Flask(__name__)

aws_access_key_id = open("C:\\Users\\gabri\\OneDrive\\Desktop\\key.txt", "r").read()
aws_secret_access_key = open("C:\\Users\\gabri\\OneDrive\\Desktop\\secretkey.txt", "r").read()
aws_session_token = open("C:\\Users\\gabri\\OneDrive\\Desktop\\token.txt", "r").read()
client = boto3.resource('dynamodb', aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        aws_session_token=aws_session_token,
                        region_name='us-east-1')
tabella = client.Table('ospedali')


@application.route("/", methods=['GET', 'POST'])
def hello():
    patient = request.json
    if patient is not None:
        patients.append(patient.__getitem__(0))
    print(patients)
    GoogleL.run()
    hospital = ConnectionDB.read_items(tabella)
    giorno = time.strftime("%d/%m/%Y")
    ora = time.strftime("%H:%M:%S")

    return render_template('page1.html', hospital=hospital, patient=patients, giorno=giorno, ora=ora)


if __name__ == "__main__":
    application.run(port=80, debug=True)
