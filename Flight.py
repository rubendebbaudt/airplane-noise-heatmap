import geopy
import geopy.distance
from Point import Point


class Flight:
    def __init__(self, latitude, longitude, geo_altitude, heading, velocity, vertical_rate):
        self.latitude = latitude
        self.longitude = longitude
        self.geo_altitude = geo_altitude
        self.heading = heading
        self.velocity = velocity
        self.vertical_rate = vertical_rate

    def position(self, time):
        start = geopy.Point(self.latitude, self.longitude)
        distance = geopy.distance.distance(meters=self.velocity * time)
        altitude = self.geo_altitude + (time * self.vertical_rate)
        end = distance.destination(point=start, bearing=self.heading)

        return Point(end[0], end[1], altitude)
