# ISS_tracker

## Description

This project is a web application that uses NASA's predicated ISS trajectory data to track the speed and location of the ISS, and can also print other interesting details about the data. 

## Project Files

This project contains 2 scripts, a dockerfile, a "requirements.txt" file, a docker-compose file, as well as a helpful diagram.
1. iss_tracker.py: contains 10 functions that are used in the web application
2. test_iss_tracker.py: contains 1-3 unit tests for each function in iss_tracker.py
3. Dockerfile: used to build docker images to your dockerhub account. Eventually these images can be used to create a container to run the code
4. docker-compose.yml: used to run our multi-container code
5. requirements.txt: contains all required libraries and packages needed to run the project

Below is a diagram that illustrates project contents.

'''
ISS_Tracker/
├── Dockerfile
├── README.md
├── diagram.png
├── docker-compose.yml
├── iss_tracker.py
├── requirements.txt
└── test
    └── test_iss_tracker.py
'''


## The Data

The data is called ISS trajectory Data and can be found on Nasa's Spot the Station (1). This data contains:
1. A header which describes ...
2. A metadata section which ...
3. A comment section for useful information about launches of the ISS or anything else
4. A list of about 6000 state vectors. These contain the predicted time, position, and speed of the ISS over a time span of about 15 days. It is updated approximately 3 times per week so that it stays accurate.
It can be accessed at this url [https://spotthestation.nasa.gov/trajectory_data.cfm](https://spotthestation.nasa.gov/trajectory_data.cfm). It can be exported as a xml or a txt.

## How to Run

### Running Containerized Code
In order to run the program, you need to use the dockerfile to build an image using the following command:
```
docker build -t <dockerhubusername>/iss_tracker:1.0 .
```
Now that the image is saved in your dockerhub as iss_tracker version 1.0, you can run the container to see the output.
```
docker run --name "iss_tracker_app" \
                      -d -p <port_number_on_vm>:<port_number_in_container> \
                      <dockerhubusername>/iss_tracker:1.0
```
In class, the specified port numbers were 5000:5000, but it can be changed to what works for your computer.
When you want to stop your container and remove it, use the commands:
```
docker stop <container_ID>
docker rm <container_ID>
```

### Curl Commands

The user will use "curl" commands to interact with the app. The curl commands look like:
```
curl localhost:<port_number>/<url_parameters>
```
The following url parameters are accepted: 
1) /epochs?limit=int&offset=int
2) /epochs/<epoch>
3) /epochs/<epoch>/speed
4) /now

## Output

Using the route "/epochs?limit=int&offset=int", the user can recieve a list of epochs of length "limit" that starts at the "offset". The default for offset is 0 and the default for limit is the lenth of the dataset, so when this command is run without query parameters, it will return the entire dataset in the form of a list of epochs. Here is an example of the expected output for limit = 2, and offset = 10.

```
curl localhost:5000/epochs?limit=2&offset=10
```
```
abcdefghijklmnopqrstuv
```

The route "/epochs/<epoch>" will return the state vectors for a specific epoch. The epochs are dictionaries that look like:
```
{
"EPOCH" : "<timestamp>", 
"X" : {"@units" : "km", "#text": "<x_coordinates>"},
"Y" : {"@units" : "km", "#text": "<y_coordinates>"},
"Z" : {"@units" : "km", "#text": "<z_coordinates>"},
"X_DOT" : {"@units" : "km/s", "#text": "<x_velocity>"},
"Y_DOT" : {"@units" : "km/s", "#text": "<y_velocity>"},
"Z_DOT" : {"@units" : "km/s", "#text": "<z_velocity>"},
}
```
The coordinates are in the J2000 reference frame.
The route "/epochs/<epoch>/speed" will return the speed for the given epoch in km/s.
Finally, the route "/now" will return the state vectors and the instantaneous speed for the epoch that is nearest to the time when the function is run.

## Citations

(1) NASA (2024) ISS Trajectory Data. Nasa's Spot the Station. [https://spotthestation.nasa.gov/trajectory_data.cfm](https://spotthestation.nasa.gov/trajectory_data.cfm)https://spotthestation.nasa.gov/trajectory_data.cfm
