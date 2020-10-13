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
            id_ambulance = 0
            km, id_ambulance = calculate_distance(patient)
            if km is None:
                print("ambulanze non disponibili")
                time.sleep(5)
                print("riprovo")
            else:
                print(id_ambulance)
                tempo = calculate_time(km)
                time.sleep(tempo)
                release_ambulance(id_ambulance)
                print('ambulanza è libera')
                return


def release_ambulance(id_ambulance):
    for ambulance in ambulances:
        if ambulance['Id'] == id_ambulance:
            ambulance['In Use'] = 0


def take_coordination_patient():
    global data
    global ambulances
    with open('attributes.json') as patients:
        data = json.load(patients)
        patients.close()
    with open('ambulanze.json') as ambulance:
        ambulances = json.load(ambulance)
        ambulance.close()


def calculate_distance(current_patient):
    first = 0
    km = 0

    coord_patient = (current_patient['Latitud'], current_patient['Longitud'])
    for current_ambulance in ambulances:
        if current_ambulance['In Use'] == 0:
            coord_ambulance = (current_ambulance['Latitud'], current_ambulance['Longitud'])
            current_km = geodesic(coord_patient, coord_ambulance).kilometers
            if first == 0:
                first = 1
                km = current_km
                previus_ambulance = current_ambulance
                id_ambulance = current_ambulance['Id']
                threadLock.acquire()
                current_ambulance['In Use'] = 1
                threadLock.release()
            elif km > current_km:
                km = current_km
                id_ambulance = current_ambulance['Id']
                threadLock.acquire()
                previus_ambulance['In Use'] = 0
                previus_ambulance = current_ambulance
                current_ambulance['In Use'] = 1
                threadLock.release()

    if first == 0:
        return None, None
    return km, id_ambulance


def calculate_time(km):
    tempo = km / vel_ambVP + km / vel_ambVO
    return tempo


take_coordination_patient()
for patient in data:
    thread = IlMioThreadMaps(patient)
    thread.start()
