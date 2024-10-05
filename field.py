from typing import List
from geopy.distance import geodesic
import math
import matplotlib.pyplot as plt
from matplotlib.collections import PathCollection ## only for typehint
from player import Player



class Corner:
        def __init__(self, ) -> None:
            self.latitude: float = 0.0
            self.longitute: float = 0.0
            self.x: float = 0.0
            self.y: float = 0.0

class Field:

    def __init__(self) -> None:
        #this cordinates are in lat and long
        #we need to to an interior orientation to convert it to pixels in the screen
        self.corners: List[Corner] = []
        self.plot_width: float = 800
        self.plot_height: float = 600

        self.minLat: float = 0
        self.maxLat: float = 0
        self.minLong: float = 0
        self.maxLong: float = 0

        ## converting things to pixels
        self.fieldwidth_inMeters: float = 0
        self.fieldlength_inMeters: float = 0
        self.field_length_px: float = 0.0
        self.field_width_px: float = 0.0
        self.field_left: float = 0.0
        self.field_top: float = 0.0

        ## Players List
        self.players: List[Player] = []

    def AppendCorner(self,lat: float, long: float ) -> None:
        corner = Corner()
        corner.latitude = lat
        corner.longitute = long
        self.corners.append(corner)
    
    def AppendPlayer(self, player: Player) -> None:
        self.players.append(player)

    def CalculateMinMaxCornersLatLong(self):
        #1° Check the min an max lat from the coorners
        for i in range(0,4):
            if i == 0:
                self.minLat = self.corners[i].latitude
                self.maxLat = self.corners[i].latitude
                self.minLong = self.corners[i].longitute
                self.maxLong = self.corners[i].longitute
            else:
                # Update min and max latitudes
                if self.corners[i].latitude < self.minLat:
                    self.minLat = self.corners[i].latitude
                if self.corners[i].latitude > self.maxLat:
                    self.maxLat = self.corners[i].latitude
                
                # Update min and max longitudes
                if self.corners[i].longitute < self.minLong:
                    self.minLong = self.corners[i].longitute
                if self.corners[i].longitute > self.maxLong:
                    self.maxLong = self.corners[i].longitute
    
    def LatLongToPixelCorners(self, lat: float, long:float) -> tuple[float, float]:
        x = (long - self.minLong) / (self.maxLong - self.minLong) * self.field_length_px
        y = (lat - self.maxLat) / (self.maxLat - self.minLat) * self.field_width_px 
        return x, y
    
    def LatLongToPixelTests(self, lat: float, long:float) -> tuple[float, float]:

        constantDegreeLat = 111139
        lat_rad = math.radians(self.maxLat)
        meters_per_degree_long = 111319 * math.cos(lat_rad)

    # Scale for meters to pixels
        scale_x = self.field_length_px / self.fieldlength_inMeters
        scale_y = self.field_width_px / self.fieldwidth_inMeters

        #first calculate the distance in meters from the first corner
        diff_x = abs(self.minLong - long)
        diff_y = abs(self.minLat - lat)

        ##convert it to meters
        distMeters_X = diff_x * constantDegreeLat
        distMeters_Y = diff_y * meters_per_degree_long

        #convert to pixels
        x = distMeters_X * scale_x
        y = distMeters_Y * scale_y
        return x, y

    def GetFieldSpecsInMeters(self):

        constantDegreeLat = 111139
        lat_rad = math.radians(self.maxLat)
        meters_per_degree_long = 111319 * math.cos(lat_rad)

        self.fieldlength_inMeters = (self.maxLat - self.minLat) * constantDegreeLat
        self.fieldwidth_inMeters = (self.maxLong - self.minLong) * meters_per_degree_long

    def draw_soccer_field(self, ax: plt.Axes):
        ##ATTENTION I DONT UNDERSTAND ALMOST ANYTHING ABOUT THIS CODE NEED TO TALK ABOUT IT

        # Standard soccer field dimensions in meters
        field_length_m = self.fieldlength_inMeters
        field_width_m = self.fieldwidth_inMeters

        # Scale factors
        field_length_px = 3840 * 0.75
        field_width_px = field_length_px / (field_length_m / field_width_m)  # Maintain aspect ratio
        self.field_length_px = field_length_px
        self.field_width_px = field_width_px

        # Field position this is for 4k pixels
        field_left = (3840 - field_length_px) / 2
        self.field_left = field_left
        field_top = (2160 - field_width_px) / 2
        self.field_top = field_top

        rect = plt.Rectangle((field_left, field_top), field_length_px, field_width_px, edgecolor='black', facecolor='none', lw=2)
        ax.add_patch(rect)

        # Scale for meters to pixels
        scale_x = field_length_px / field_length_m
        scale_y = field_width_px / field_width_m

        # Center Circle
        center_circle_radius_m = 9.15  # Standard center circle radius
        center_circle = plt.Circle((3840 / 2, 2160 / 2), center_circle_radius_m * scale_x, color='black', fill=False, lw=2)
        ax.add_patch(center_circle)

            # Goal Areas (6-yard box)
        goal_area_length_m = 5.5
        goal_area_width_m = 18.32
        goal_area_left = plt.Rectangle((field_left, 2160 / 2 - (goal_area_width_m * scale_y / 2)), 
                                    goal_area_length_m * scale_x, goal_area_width_m * scale_y, 
                                    edgecolor='black', facecolor='none', lw=2)
        goal_area_right = plt.Rectangle((3840 - field_left - goal_area_length_m * scale_x, 2160 / 2 - (goal_area_width_m * scale_y / 2)), 
                                        goal_area_length_m * scale_x, goal_area_width_m * scale_y, 
                                        edgecolor='black', facecolor='none', lw=2)
        ax.add_patch(goal_area_left)
        ax.add_patch(goal_area_right)

        # Vertical Center Line
        plt.plot([3840 / 2, 3840 / 2], [field_top, field_top + field_width_px], color='black', lw=2)

    def CreatePlayerField(self, ax: plt.Axes) -> PathCollection:
        playerPoint = ax.scatter(self.field_left,self.field_top , marker="o")
        return playerPoint
    
    def UpdatePlayerPosition(self, player: PathCollection, x:float, y:float) -> None:
        player.set_offsets([self.field_left + x, self.field_top + y])



