# Package-delivery-program
Scenario description:
-
This python program was made to address the following scenario within the given constraints:

You own a delivery service that has three trucks, two drivers, and an average of 40 packages to deliver each day; each package has specific criteria and delivery requirements.

The delivery addresses for the 40 packages to be delivered are listed in the packages.csv file. The distances between each address are listed in the distances.csv file.

Your task is to determine the best algorithm, write code, and present a solution where all 40 packages will be delivered on time with the least number of miles added to the combined mileage total of all trucks.

Constraints:
-



1. Take into consideration the specific delivery time expected for each package, as well as the possibility that delivery requirements, such as the expected delivery time, can be changed by management at any time and at any point along the chosen route.
2. The program user should be able to see the progress of each truck and its packages at the time entered by the user. This should include what has been delivered and when the delivery took place.
3. Trucks travel at an average speed of 18 miles per hour.
4. Each truck can carry a maximum of 16 packages.
5. Trucks have a unlimited fuel with no need to stop.
6. Each driver stays with the same truck as long as that truck is in service.
7. Drivers leave the hub at 8:00 a.m., with the truck loaded, and can return to the hub for packages if needed.
8. The day ends when all 40 packages have been delivered.
9. Delivery time is instantaneous, i.e., no time passes while at a delivery (that time is factored into the average speed of the trucks).
10. There is up to one special note for each package.
11. The wrong delivery address for package #9, Third District Juvenile Court, will be corrected at 10:20 a.m. The correct address is 410 S State St., Salt Lake City, UT 84111.
12. The package ID is unique; there are no collisions.

   


