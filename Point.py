from math import sqrt
from geopy import distance

class Point:
    def __init__(self, latitude, longitude, altitude):
        self.latitude = latitude # decimal
        self.longitude = longitude # decimal
        self.altitude = altitude # in meters

    def distance(self, point):
        plane_point = (self.latitude, self.longitude)
        ground_point = (plane.latitude, plane.longitude)
        result = sqrt((distance.distance(plane_point, ground_point).m)**2 + (self.altitude-point.altidude)**2)
        return result # in meters
