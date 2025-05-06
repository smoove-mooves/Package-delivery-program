import csv

from datetime import datetime, timedelta

########################################################################################################################
# Hash table class
########################################################################################################################


class ChainingHashTable:
    # Function initializes the size of the hash table's capacity
    def __init__(self, initial_capacity=41):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Function returns a string of a package object's data
    def __str__(self):
        output = ""
        for i, bucket in enumerate(self.table):
            if not bucket:
                output += "Empty\n"
            else:
                for kv in bucket:
                    output += f"{kv[1]}\n"
        return output

    # Function inserts a package object into the hash table
    def insert(self, package_id, item):
        bucket = package_id
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == package_id:
                kv[1] = item
                return True

        key_value = [package_id, item]
        bucket_list.append(key_value)
        return True

    # Function returns a package object's attributes by searching the hash table for the package's package ID
    def search(self, package_id):
        bucket = package_id
        bucket_list = self.table[bucket]

        for kv in bucket_list:

            if kv[0] == package_id:
                return kv[1]
        return None

    # Function removes a package from the hash table based on the package's package ID
    def remove(self, package_id):
        bucket = package_id
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == package_id:
                bucket_list.remove([kv[0], kv[1]])


# Creates a hash table object called myHash
myHash = ChainingHashTable()

########################################################################################################################
# Package class
########################################################################################################################


class Package:
    # package object constructor
    def __init__(self, package_id, address, city, state, package_zip, deadline, weight, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.package_zip = package_zip
        self.deadline = deadline
        self.weight = weight
        self.status = status

    # Function returns a string of a package object's data
    def __str__(self):
        return (f"{self.package_id}, {self.address}, {self.city}, {self.state}, "
                f"{self.package_zip}, {self.deadline}, {self.weight}, {self.status}")

########################################################################################################################
# Function to load package data from the csv file into the myHash hash table object
########################################################################################################################


def load_package_data(filename):
    max_id = 0
    with open(filename) as packages:
        packageData = csv.reader(packages, delimiter=',')
        next(packageData)
        for package in packageData:
            pID = int(package[0])
            if pID > max_id:
                max_id = pID
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pStatus = package[7]

            package = Package(pID, pAddress, pCity, pState, pZip, pDeadline, pWeight, pStatus)

            myHash.insert(pID, package)

            if max_id >= len(myHash.table):
                new_capacity = max_id + 1
                new_table = [[] for _ in range(new_capacity)]

                for bucket in myHash.table:
                    for kv in bucket:
                        new_bucket = kv[0] % new_capacity
                        new_table[new_bucket].append(kv)

                myHash.table = new_table


load_package_data("packages.csv")

########################################################################################################################
# Section to get user input
########################################################################################################################

# Gathers the users current time
current_time = input("Enter the current time in 24hr time format(HH:MM:SS) "
                     "to get an accurate delivery status of packages:")
h, m, s = map(int, current_time.split(":"))
current_user_time = datetime.now().replace(hour=h, minute=m, second=s)
# Statements to change package 9's delivery address when the user's time is after 10:20 A.M.
package_9_update = datetime.now().replace(hour=10, minute=20, second=00)
package_9 = myHash.search(9)

if current_user_time >= package_9_update:
    package_9.address = '410 S State St'


# Function sets the delivery status of all packages to 'En route' if the truck has left the hub
def en_route(truck_object):
    if current_user_time >= truck_object.departure_time:
        loaded_packages = truck_object.packages
        for package_id in loaded_packages:
            en_route_package = myHash.search(package_id)
            en_route_package.status = "En route"

########################################################################################################################
# Truck class
########################################################################################################################


# truck object constructor
class Truck:
    def __init__(self, truck_id, distance_traveled, packages, speed, current_address, departure_time):
        self.truck_id = truck_id
        self.distance_traveled = distance_traveled
        self.packages = packages
        self.speed = speed
        self.current_address = current_address
        self.departure_time = departure_time

    # Function returns a string of a truck object's data
    def __str__(self):
        return f"({self.truck_id}, {self.distance_traveled}, {self.packages}, {self.speed}, {self.current_address}, {self.departure_time})"


# truck_1 contains all packages with deadlines before EOD, but the packages have no delays
truck_1 = Truck(1, 0.0, [1, 13, 14, 15, 16, 20, 19, 29, 30, 31, 34, 37, 40], 18.0,
                '4001 South 700 East', datetime.now().replace(hour=8, minute=00, second=00))

# truck_2 contains all packages that can only be on Truck 2
truck_2 = Truck(2, 0.0, [3, 18, 36, 38, 25, 24, 26, 27, 33, 35, 39], 18.0,
                '4001 South 700 East', datetime.now().replace(hour=8, minute=00, second=00))

# truck_3 contains all the packages with delays
truck_3 = Truck(2, 0.0, [6, 23, 28, 32, 9, 2, 4, 5, 7, 8, 10, 11, 12, 17, 21, 22], 18.0,
                '4001 South 700 East', datetime.now().replace(hour=10, minute=21, second=00))
# en_route function calls for each truck to change the delivery status of truck package's
# to 'en_route' if the user's time is after a truck's departure time
en_route(truck_1)
en_route(truck_2)
en_route(truck_3)

########################################################################################################################
# Function to load distances.csv data
########################################################################################################################

# Declaration of an empty list to store distance data
distance_data = []


def load_distance_data():
    with open('distances.csv', 'r') as file:
        distance_reader = csv.reader(file)
        for row in distance_reader:
            distance_data.append(row)


# Function call to upload distance data
load_distance_data()


########################################################################################################################
# Function search the distance between two addresses
########################################################################################################################


def distance_search(address_y, address_x):
    distance = distance_data[address_y][address_x]
    return distance


########################################################################################################################
# Function to load addresses.csv data and function to get address id
########################################################################################################################

# Declaration of an empty list to store address data
address_data = []


def load_address_data():
    with open('addresses.csv', 'r') as file:
        address_reader = csv.reader(file)
        for row in address_reader:
            address_data.append(row)


# Function call to load address data
load_address_data()


########################################################################################################################
# Function to get the address id from an address's string
########################################################################################################################

def get_address_id(address_string):
    for row in address_data:
        if address_string in row:
            selected_id = row[1]
            return int(selected_id)


########################################################################################################################
# Function to find the nearest neighbor's address
########################################################################################################################

def get_closest_address(address_x):
    temporary_distances_list = []
    top_row = distance_data[0]
    selected_row = distance_data[address_x]
    for item in distance_data[address_x]:
        temporary_distances_list.append(item)

    del temporary_distances_list[0]
    del temporary_distances_list[0]
    del temporary_distances_list[-1]
    min_distance = min(temporary_distances_list)

    nearest_neighbor = top_row[selected_row.index(min_distance)]
    return nearest_neighbor


########################################################################################################################
# Function to get a package's address string from the package id
########################################################################################################################

def get_address_string(package_id):
    selected_package = myHash.search(package_id)
    return selected_package.address.strip()


########################################################################################################################
# Function to deliver packages on a truck
########################################################################################################################


def deliver_truck_packages(truck_object):
    # Sets the non-delivered packages to the packages currently loaded in the truck object
    packages_not_delivered = truck_object.packages
    # Declaration of empty lists used to store data used in this function
    address_strings = []
    address_ids = []
    address_distances = []
    # Sets the initial address ID to 1 which represents the hub/starting address of each truck object
    address_y = 1
    # Code to calculate how long each truck has traveled for
    time_traveled = current_user_time - truck_object.departure_time
    seconds_traveled = time_traveled.total_seconds() / 3600
    miles_traveled = seconds_traveled * 18.0

    # While loop to ensure the delivery code runs as long as there are packages loaded in the truck object
    while len(truck_object.packages) > 0:
        # Gets the address for each package in the truck object
        for item in packages_not_delivered:
            address_strings.append(get_address_string(item))
        # Gets the address ID for each package's address string
        for item in address_strings:
            address_ids.append(get_address_id(item))
        # Calculates the closest address to the truck by determining the smallest distance in the address_distances list
        for item in address_ids:
            address_distances.append(float(distance_search(address_y, int(item))))
            min_distance = min(address_distances)
            min_distance_index = address_distances.index(min_distance)
            nearest_neighbor = packages_not_delivered[min_distance_index]
        # Code that updates necessary attributes of the truck object and packages
        # if the truck object has traveled far enough
        if miles_traveled >= truck_object.distance_traveled:
            package_travel_time = int(round((min_distance / 18.0) * 60))
            minutes_delta = timedelta(minutes=package_travel_time)
            package_delivery_time = truck_object.departure_time + minutes_delta
            package_to_update = myHash.search(nearest_neighbor)
            package_to_update.status = "Delivered at " + datetime.strftime(package_delivery_time, '%H:%M:%S')
            truck_object.packages.remove(nearest_neighbor)
            truck_object.distance_traveled += min_distance
            address_y_string = str(myHash.search(nearest_neighbor).address)
            address_y = get_address_id(address_y_string)
            address_strings.clear()
            address_ids.clear()
            address_distances.clear()
        else:
            break


# Function calls to deliver the packages for truck 1,2 and 3
deliver_truck_packages(truck_1)
deliver_truck_packages(truck_2)
deliver_truck_packages(truck_3)
# Variable declaration that stores the total miles traveled by all trucks
total_truck_mileage = truck_1.distance_traveled + truck_2.distance_traveled + truck_3.distance_traveled
# Variable declaration to set the parameter for the get_packages_status function
i = 1


# Function to display the attributes of every package by iterating through the hash table using package IDs
def get_packages_status(i):
    while i <= 40:
        print(myHash.search(i))
        i = i + 1


# Input to allow the user to choose between searching the status of one package or all packages
user_choice = input("Would you like to search the status of an individual package or see the status of all packages?\n"
                    "For an individual package enter 'Individual'. For all packages enter 'All'"
                    "\n:")
# Logic to display package status based on what the user chooses
if user_choice == "All":
    print("Package ID,Address,City,State,Zip,Delivery Deadline,Weight,Status")
    get_packages_status(i)
    print("Total mileage of all trucks combined: " + str(total_truck_mileage))

if user_choice == "Individual":
    selected_package_id = int(input("Enter the package ID of the package you would like to see the status of."))
    print("Package ID,Address,City,State,Zip,Delivery Deadline,Weight,Status")
    print(myHash.search(selected_package_id))
    print("Total mileage of all trucks combined: " + str(total_truck_mileage))
