#!/usr/bin/env python3

# Kaushal Kishore (bithack)
# 111601008
# Lab2 - Question No. 2

import numpy as np
import heapq

def getSpeed(x):
    return np.exp(0.5*x) / (1 + np.exp(0.5*x)) + 15 / (1 + np.exp(0.5*x))

class Vehicle:
    def __init__(self , _vehicle_idx , _path):
        self.vehicle_idx = _vehicle_idx
        self.next_location_idx = 0
        self.speed = 0
        self.path = _path       # creating a shallow copy to avaoid redundancy
        self.entry_time = [None] * len(self.path)
        
        
    def changeRoad(self):
        self.next_location_idx += 1

    def changeSpeed(self, _speed):
        self.speed = _speed

    def isDestinationReached(self):
        if self.next_location_idx > 4:
            return True
        return False

    def setRecentEntryTime(self , t):
        self.entry_time[self.next_location_idx-1] = t
    
    def getCurrentPath(self):
        # print("Returning the current Path: " , \
        # self.path[self.next_location_idx-1] , self.path[self.next_location_idx])
        if self.next_location_idx!=0 and self.isDestinationReached()==False:
            return (self.path[self.next_location_idx-1] , self.path[self.next_location_idx])
        return (self.path[0] , self.path[1])

    def __repr__(self):
        repr_str = "{0}".format(self.vehicle_idx)
        n = len(self.path)
        for i in range(n):
            repr_str = repr_str + ",{0}".format(round(self.entry_time[i],10))
        
        # print("__repr__: " , self.path , end=" " )
        return repr_str


class RoadNetwork:
    '''
        road:
            Contains weighted adjacency matrix M, where each entry M(i,j) 
            denotes the length of the road between i and j. The value M(i,j) 
            0 means no connection between i and j.

        time:
            Contains the timestamp in minutes of a vehicle starting from a particular node.

        vehicle:
            A list of list where each row correspond to the vehicle corresponding to that index value
            represents the path taken by the agent.       
        
        vehicle_speed:
            List containing the current speed of the vehicle.
    '''
    
    def __init__(self):
        self.road = np.array(np.load('/home/kaushal/Documents/git/ailab/week2/traffic/road' , encoding='bytes'))
        # self.road = np.array(np.loadtxt('./txt/road.txt'))

        # self.timestamp = np.array(np.load('./traffic/time' , encoding='bytes')).flatten().tolist()

        t = np.array(np.load('/home/kaushal/Documents/git/ailab/week2/traffic/time' , encoding='bytes')) / 60
        # t = np.array(np.loadtxt('./txt/time.txt')) / 60

        self.timestamp = np.hstack((t , np.arange(t.shape[0]).reshape(-1,1))).tolist()
        self.timestamp = [tuple(x) for x in self.timestamp] 
        del t

        heapq.heapify(self.timestamp)
        # print(self.timestamp)

        self.vehicle_path = np.array(np.load('/home/kaushal/Documents/git/ailab/week2/traffic/vehicle' , encoding='bytes')).tolist()
        # self.vehicle_path = np.array(np.loadtxt('./txt/vehicle.txt')).tolist()

        n = self.getNumVehicle()

        self.vehicle = [Vehicle(i , self.vehicle_path[i]) for i in range(n)]
        self.traffic = np.zeros_like(self.road)
        

        # self.vehicle_speed = [None] * self.getNumVehicle()
        # self.vehicle = [ for x in self.vehicle_path]

    def getNumRoad(self):
        return self.road.shape[0]
    
    def getNumVehicle(self):
        return len(self.vehicle_path)

    def simulate(self):
        count = 0
        while len(self.timestamp) != 0:
            count += 1
            # print("\n-----------------------------\nCycle: {0}".format(count))

           

            # t here is a tuple of the form : (time, vehicle index)
            t = heapq.heappop(self.timestamp)
            # print("Current Timestamp: " , self.timestamp)
            # retrieve a new vehicle
            curr_vehicle = self.vehicle[int(t[1])]
            
            # if vehicle has not reached to the destination
            if curr_vehicle.entry_time[curr_vehicle.next_location_idx] == None:

                # get number of vehicles ahead in the path
                prev_path = curr_vehicle.getCurrentPath()
                # num_vehicle_ahead = self.traffic[prev_path]

                # change the road
                curr_vehicle.changeRoad()

                # Current path
                curr_path = curr_vehicle.getCurrentPath()
                num_vehicle_ahead = self.traffic[curr_path]

                # reduce the traffic of the previous path
                if self.traffic[prev_path]!=0 and curr_path != prev_path:
                    self.traffic[prev_path] -= 1

                
                # setting the entry time for recent location
                curr_vehicle.setRecentEntryTime(t[0]) 

                if curr_vehicle.isDestinationReached() == False:
                    # setting the speed of the vehicle
                    curr_vehicle.changeSpeed(getSpeed(num_vehicle_ahead))

                    self.traffic[curr_path] = self.traffic[curr_path] + 1

                    # pushing the timestamp of this vehicle on reaching the next location into the heap
                    distance_of_crrent_path = self.road[curr_path]

                    # calculate time to traverse to new location
                    time = distance_of_crrent_path / curr_vehicle.speed

                    # print(t)
                    # pushing the arrival timestamp to the list
                    # print(t[0] , time)
                    # print("Vehicle Index: ", int(t[1]))
                    # print("speed: ", curr_vehicle.speed)
                    # print("Current Distance Path: {0}".format(distance_of_crrent_path))
                    # print("Pushing timestamp: " , (t[0] + time, t[1]))
                    # print("Vehicle Ahead: " , num_vehicle_ahead)
                    # print("\n\n")
                    heapq.heappush(self.timestamp , (t[0] + time, t[1]))
                    # if 0 <= count <= 1000 :
                    #     print("Current Path: ", curr_path)
                    #     print(self.traffic)
                

            self.vehicle[int(t[1])] = curr_vehicle

        n = self.getNumVehicle()
        for i in range(n):
            print(str(self.vehicle[i]))
            pass


r = RoadNetwork()
print("Vehicle, site1,site2,site3,site4,site5")
r.simulate()
