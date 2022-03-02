
import requests
import json
import random
import time


edgexip = '127.0.0.1'
humval = 40
tempval = 23

def generateSensorData(humval, tempval):

    humval = random.randint(humval-6,humval+6)
    tempval = random.randint(tempval-2, tempval+2)

    print("Sending values: Humidity %s, Temperature %sC" % (humval, tempval))

    return (humval, tempval)



if __name__ == "__main__":

    sensorTypes = ["temperature", "humidity"]

    while(1):

        (humval, tempval) = generateSensorData(humval, tempval)

        url = 'http://%s:49986/api/v1/resource/Temp_and_Humidity_sensor_cluster/temperature' % edgexip
        payload = tempval
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
        print(response)

        url = 'http://%s:49986/api/v1/resource/Temp_and_Humidity_sensor_cluster/humidity' % edgexip
        payload = humval
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
        print(response)
        time.sleep(5)
