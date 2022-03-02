import csv
import json
import time
import pandas as pd
import numpy as np
import keras
import requests
from keras.models import Sequential
from keras.layers import Input,Dense,Dropout
from keras.wrappers.scikit_learn import KerasRegressor


line_count_humidity = 0
line_count_temperature = 0
edgexip = '127.0.0.1'


def read_data():
    global line_count_humidity, line_count_temperature
    humidity, temperature = None, None
    with open('./humidity.csv', 'r+', newline='') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for i, row in enumerate(csv_reader):
            if line_count_humidity == i:
                humidity = row[0]
                line_count_humidity += 1
                break
        f.close()

    with open('./temperature.csv', 'r+', newline='') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for i, row in enumerate(csv_reader):
            if line_count_temperature == i:
                temperature = row[0]
                line_count_temperature += 1
                break
        f.close()

    return [int(humidity), int(temperature)]


def predict(data):

    return model.predict(np.array([data]))


def send_command(data):
    url = 'http://%s:49986/api/v1/resource/Temp_and_Humidity_sensor_cluster/power' % edgexip
    payload = str(data)
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
    print(str(data), response)


if __name__ == "__main__":
    model = keras.models.load_model('/home/huyquang/DATN-EdgeX/edgex.pb')
    while True:
        data = read_data()
        result = model.predict(np.array([data]))
        print(result[0][0])
        send_command(result[0][0])
        time.sleep(2)
