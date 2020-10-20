import boto3
from geopy.distance import geodesic
from threading import Thread
import threading
import time
import json
from Cloud import ConnectionDB

vel_ambVP = 0.033  # Km/s corrispondente a 120 km/h
vel_ambVO = 0.025  # Km/s corrispondente a 90 km/h

sem = threading.Semaphore(1)
aws_access_key_id = open("C:\\Users\\gabri\\OneDrive\\Desktop\\key.txt", "r").read()
aws_secret_access_key = open("C:\\Users\\gabri\\OneDrive\\Desktop\\secretkey.txt", "r").read()
aws_session_token = open("C:\\Users\\gabri\\OneDrive\\Desktop\\token.txt", "r").read()
client = boto3.resource('dynamodb', aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        aws_session_token=aws_session_token,
                        region_name='us-east-1')
tabella = client.Table('ospedali')


class IlMioThreadMaps(Thread):
    patient = {}

    def __init__(self, current_patient):
        Thread.__init__(self)
        self.patient = current_patient

    def run(self):
        while True:
            km, id_hospital = calculate_distance(self.patient)
            if km is None:
                print("ambulanze non disponibili")
                time.sleep(5)
                print("riprovo")
            else:
                print(id_hospital)
                tempo = calculate_time(km)
                time.sleep(tempo)
                sem.acquire()
                release_ambulance(id_hospital)
                sem.release()
                print('ambulanza è libera')
                return


def release_ambulance(id_ambulance):

    ConnectionDB.update_item(tabella, id_ambulance, 1)


def take_coordination_patient():
    global data
    with open("C:\\Users\\gabri\\untitled\\attributes.json") as patients:
        data = json.load(patients)
        patients.close()


def calculate_distance(current_patient):
    first = 0
    km = 0
    coord_patient = (current_patient['Latitud'], current_patient['Longitud'])
    sem.acquire()
    hospital = ConnectionDB.read_items(tabella)
    for current_Hospital in hospital:
        if current_Hospital['NumA'] != 0:
            coord_ambulance = (current_Hospital['Latitud'], current_Hospital['Longitu'])
            current_km = geodesic(coord_patient, coord_ambulance).kilometers
            if first == 0:
                first = 1
                km = current_km
                previus_hospital = current_Hospital
                id_hospital = current_Hospital['Id']
            elif km > current_km:
                km = current_km
                id_hospital = current_Hospital['Id']
                previus_hospital = current_Hospital
    if first != 0:
        ConnectionDB.update_item(tabella, id_hospital, 0)
    sem.release()
    if first == 0:
        return None, None
    return km, id_hospital


def calculate_time(km):
    tempo = km / vel_ambVP + km / vel_ambVO
    return tempo


def run():
    take_coordination_patient()
    for patient in data:
        thread = IlMioThreadMaps(patient)
        thread.start()
