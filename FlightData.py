import time
from opensky_api import OpenSkyApi
from time import sleep
import xlsxwriter
import numpy as np

time = int(time.time())

# Variabelen
START_TIME = time
DURATION = 900 #in seconds
RESOLUTION = 30 #in seconds
LA_MIN = 49.9028
LA_MAX = LA_MIN + 2
LO_MIN = 3.4862
LO_MAX = LO_MIN +2
OS_USER = #put login here
OS_PASS = #put pass here

data = np.empty((0, 6), int)

api = OpenSkyApi(OS_USER, OS_PASS)
for x in range(START_TIME - DURATION, START_TIME, RESOLUTION):
    # bbox = (min latitude, max latitude, min longitude, max longitude)
    states = api.get_states(time_secs=x, bbox=(LA_MIN, LA_MAX, LO_MIN, LO_MAX))
    if states:
        for s in states.states:
            if s.latitude and s.longitude and s.geo_altitude and s.heading and s.velocity and s.vertical_rate:
                data = np.append(data, np.array([[s.latitude, s.longitude, s.geo_altitude, s.heading, s.velocity, s.vertical_rate]]), axis=0)
    sleep(1)

print("Data gathered, creating excel...")

# Latitude;Longitude;Geo Altitude; Heading; Velocity; Vertical Rate
workbook = xlsxwriter.Workbook('FlightData.xlsx')
worksheet = workbook.add_worksheet()

col = 0

for row, data in enumerate(data):
    worksheet.write_row(row, col, data)

workbook.close()
