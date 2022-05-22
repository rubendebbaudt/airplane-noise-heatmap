import numpy as np
import math
from Flight import Flight
from Point import Point
import gmplot

ALPHA = 0.0005
D1 = 1
p0 = 2E-5  # Pa
AMBIENT_NOISE = 40  # dB
LA_MIN = 49.9028
LA_MAX = LA_MIN + 2
LO_MIN = 3.4862
LO_MAX = LO_MIN + 2
MATRIX_G = 100
RESOLUTION = 30  # in seconds


# dB CALCULATION
def dB_to_Pa(L):
    p = p0 * 10 ** (L / 20)  # Pa
    return p


def sound_calculation(point, flight, position):
    distance = point.distance(position)
    source = flight.source

    Lmax = source - 20 * math.log10(distance / D1) - 8.69 * ALPHA * (distance - D1)
    return Lmax

lats = []
longs = []
values = []


def fill_matrix(flight, time):
    position = flight.position_calc(time)
    L1 = flight.source
    d_matrix = np.zeros((MATRIX_G, MATRIX_G))
    for x in range(len(d_matrix)):
        for y in range(len(d_matrix[0])):
            latitude = LA_MIN + (LA_MAX - LA_MIN)/MATRIX_G * y
            longitude = LO_MIN + (LO_MAX - LO_MIN)/MATRIX_G * x

            d_matrix[x][y] = position.distance(Point(latitude, longitude, 0))
    Lmax = L1 - 20 * np.log10(d_matrix / D1) - 8.69 * ALPHA * (d_matrix - D1)
    p = p0 * np.power(10 * np.ones((MATRIX_G, MATRIX_G)), Lmax / 20)
    matrix = np.square(p) / (p0 * p0)
    return matrix

test_flight = Flight(51.3566, 5.4028, 1805.94, 76.12, 135.13, 16.58)

flights = []
flights.append(test_flight)

ambient_pressure = np.ones((MATRIX_G, MATRIX_G))*(dB_to_Pa(AMBIENT_NOISE)**2)/(p0**2)
total_pressure = np.zeros((MATRIX_G, MATRIX_G))


for t in range(RESOLUTION):
    pressure = ambient_pressure
    for f in flights:
        matrix = fill_matrix(f, t)
        pressure = np.add(pressure, matrix)

    total_pressure = np.add(total_pressure, pressure)

result = 10*np.log10(total_pressure/RESOLUTION)



for x in range(MATRIX_G):
    for y in range(MATRIX_G):
        latitude = LA_MIN + (LA_MAX - LA_MIN) / MATRIX_G * y
        longitude = LO_MIN + (LO_MAX - LO_MIN) / MATRIX_G * x
        lats.append(latitude)
        longs.append(longitude)
        values.append(result[x][y])

print(lats)
print(values)

gmap = gmplot.GoogleMapPlotter(50.85045, 4.34878, 9)

gmap.heatmap(lats, longs, int(values))

gmap.draw("Planes_heatmap.html")
