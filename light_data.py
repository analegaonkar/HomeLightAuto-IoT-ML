# import pandas
from sklearn.externals import joblib
import csv
import json  # library for handling JSON data
import os.path
import time  # module for sleep operation
from datetime import datetime, date

from boltiot import Bolt

api_key = "3e4f0c87-27b8-44e7-98e9-263389baad36"
device_id = "BOLT290232"
mybolt = Bolt(api_key, device_id)


def get_sensor_value_from_pin(pin):
    """Returns the sensor value. Returns -999 if request fails
    :param pin:
    :return:
    """
    try:
        response = mybolt.analogRead(pin)
        data = json.loads(response)
        if data["success"] != 1:
            print("Request not successfull. This is the response->", data)
            # return -999
        else:
            lin_reg = joblib.load("./")
        sensor_value = int(data["value"])
        return sensor_value
    except Exception as e:
        print("Something went wrong when returning the sensor value")
        print(e)
        return -999


# response = mybolt.isOnline()
# response = mybolt.restart()
filename = "light_data.csv"

while True:
    sensor_value = get_sensor_value_from_pin("A0")
    print("The current sensor value is:", sensor_value)
    if sensor_value == -999:
        print("Skipping the request.")
        time.sleep(60)
        continue
    threshold = 350
    if sensor_value <= threshold:
        print("Sensor value has exceeded threshold")
        response = mybolt.digitalWrite(4, "HIGH")
        ls = 'ON'
    else:
        response = mybolt.digitalWrite(4, "LOW")
        ls = 'OFF'

    today = date.today().strftime("%m-%d-%Y")
    time1 = datetime.now().strftime("%H:%M:%S")
    parameters = {'Date': today, 'Time': time1, 'Threshold': threshold, 'SensorValue': sensor_value, 'LightStatus': ls}
    # print(parameters)
    with open(filename, 'a', newline='') as file:
        fieldnames = ['Date', 'Time', 'Threshold', 'SensorValue', 'LightStatus']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not os.path.isfile(filename):
            writer.writeheader()
        writer.writerow(parameters)
    # df = pandas.DataFrame(parameters)
    # df.to_csv('lightData_modified.csv')

    time.sleep(60)
