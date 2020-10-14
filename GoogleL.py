import json
from geopy.distance import geodesic
import threading
from threading import Thread
import time

vel_ambVP = 0.033  # Km/s corrispondente a 120 km/h
vel_ambVO = 0.025  # Km/s corrispondente a 90 km/h
threadLock = threading.Lock()


threadLock = threading.Lock()


class IlMioThreadMaps(Thread):
    patient = {}

    def __init__(self, current_patient):
        Thread.__init__(self)
        self.patient = current_patient

    def run(self):
        while True:
            km, id_hospital = calculate_distance(patient)
            if km is None:
                print("ambulanze non disponibili")
                time.sleep(5)
                print("riprovo")
            else:
                print(id_hospital)
                tempo = calculate_time(km)
                time.sleep(tempo)
                release_ambulance(id_hospital)
                print('ambulanza è libera')
                return


def release_ambulance(id_ambulance):
    for current_hospital in hospital:
        if current_hospital['Id'] == id_ambulance:
            current_hospital['Number of Ambulances'] = current_hospital['Number of Ambulances'] + 1


def take_coordination_patient():
    global data
    global hospital
    with open('attributes.json') as patients:
        data = json.load(patients)
        patients.close()
    with open('hospital.json') as ambulance:
        hospital = json.load(ambulance)
        ambulance.close()


def calculate_distance(current_patient):
    first = 0
    km = 0

    coord_patient = (current_patient['Latitud'], current_patient['Longitud'])
    for current_Hospital in hospital:
        if current_Hospital['Number of Ambulances'] != 0:
            coord_ambulance = (current_Hospital['Latitud'], current_Hospital['Longitud'])
            current_km = geodesic(coord_patient, coord_ambulance).kilometers
            if first == 0:
                first = 1
                km = current_km
                previus_hospital = current_Hospital
                id_hospital = current_Hospital['Id']
                threadLock.acquire()
                current_Hospital['Number of Ambulances'] = current_Hospital['Number of Ambulances'] - 1
                threadLock.release()
            elif km > current_km:
                km = current_km
                id_hospital = current_Hospital['Id']
                threadLock.acquire()
                previus_hospital['Number of Ambulances'] = previus_hospital['Number of Ambulances'] + 1
                previus_hospital = current_Hospital
                current_Hospital['Number of Ambulances'] = current_Hospital['Number of Ambulances'] - 1
                threadLock.release()

    if first == 0:
        return None, None
    return km, id_hospital


def calculate_time(km):
    tempo = km / vel_ambVP + km / vel_ambVO
    return tempo


take_coordination_patient()
for patient in data:
    thread = IlMioThreadMaps(patient)
    thread.start()
