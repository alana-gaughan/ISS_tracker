# ISS Tracker

## Description

This project is a web application that uses NASA's predicated ISS trajectory data to track the speed and location of the ISS.

## Project Diagram
![Screenshot (470)](https://github.com/alana-gaughan/ISS_tracker/assets/142938455/6df0ff7a-2d20-4461-bf46-74bf8eebad90)

## Project Files

This project contains 2 scripts, a dockerfile, a "requirements.txt" file, a docker-compose file, as well as a helpful diagram.
1. iss_tracker.py: contains functions that are used in the web application
2. test_iss_tracker.py: contains unit tests for each function in iss_tracker.py
3. Dockerfile: used to build docker images to your dockerhub account. Eventually these images can be used to create a container to run the code
4. docker-compose.yml: used to run our containers
5. requirements.txt: contains all required libraries and packages needed to run the project

Below is a diagram that illustrates project contents.

```
ISS_Tracker/
├── Dockerfile
├── README.md
├── diagram.png
├── docker-compose.yml
├── iss_tracker.py
├── requirements.txt
└── test
    └── test_iss_tracker.py
```

## The Data

The data is called ISS trajectory Data and can be found on Nasa's Spot the Station (1). This data contains list of about 6000 state vectors that can help track the international space station's location and speed. The state vectors contain the predicted time, position, and speed of the ISS over a time span of about 15 days. It is updated approximately 3 times per week so that it stays accurate.
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
Alternatively, this project contains a docker-compose.yml file which will automatically build the image and run the containers on port 5000 with a few simple commands. Before you use the docker-compose, change the dockerhub username to your own, and the port to whatever you want. Then, to run the container in the background, use the following command:
```
docker-compose up -d
```
To close the container when you are done, use the command:
```
docker-compose down
```

### Curl Commands

The user will use "curl" commands to interact with the app. The curl commands look like:
```
curl localhost:5000/<url_parameters>
```
The following url parameters are accepted: 
1) /comment
2) /header
3) /metadata
4) /epochs
5) /epochs?limit=int&offset=int
6) /epochs/(epoch)
7) /epochs/(epoch)/speed
8) /epochs/(epoch)/location
9) /now

### Outputs & Interpretations
The route "/comment" returns the list of comments that are provided by NASA. There may be various physical properties of the ISS in the comment list such as the drag coefficient, the mass, the solar radiation coefficient, etc. The comments will also include upcoming launching and docking dates among other things. Here is an example output:
```
curl localhost:5000/comment
```
```
[
  "Units are in kg and m^2",
  "MASS=459154.20",
  "DRAG_AREA=1487.80",
  "DRAG_COEFF=2.00",
  "SOLAR_RAD_AREA=0.00",
  "SOLAR_RAD_COEFF=0.00",
  "Orbits start at the ascending node epoch",
  "ISS first asc. node: EPOCH = 2024-03-15T13:05:34.170 $ ORBIT = 402 $ LAN(DEG) = 49.49781",
  "ISS last asc. node : EPOCH = 2024-03-30T10:42:10.141 $ ORBIT = 633 $ LAN(DEG) = -3.07552",
  "Begin sequence of events",
  "TRAJECTORY EVENT SUMMARY:",
  null,
  "|       EVENT        |       TIG        | ORB |   DV    |   HA    |   HP    |",
  "|                    |       GMT        |     |   M/S   |   KM    |   KM    |",
  "|                    |                  |     |  (F/S)  |  (NM)   |  (NM)   |",
  "=============================================================================",
  "71S Launch            081:13:21:19.000             0.0     425.0     412.5",
  "(0.0)   (229.5)   (222.8)",
  null,
  "71S Docking           081:16:39:42.000             0.0     425.0     412.5",
  "(0.0)   (229.5)   (222.7)",
  null,
  "SpX-30 Launch         081:20:55:09.000             0.0     425.0     412.6",
  "(0.0)   (229.5)   (222.8)",
  null,
  "SpX-30 Docking        083:11:30:00.000             0.0     425.3     412.0",
  "(0.0)   (229.6)   (222.4)",
  null,
  "=============================================================================",
  "End sequence of events"
]
```
The route "/header" returns the header of the data file which includes the date the data was created and the author of the data. Here is an example output:
```
curl localhost:5000/header
```
```
{
  "CREATION_DATE": "2024-075T20:59:30.931Z",
  "ORIGINATOR": "JSC"
}
```
The route "/metadata" returns a dictionary containing information about the data itself, like the name of the object being tracked, the reference frame, the time zone reference frame, as well as the start and stop times of the data. Here is an example output:
```
curl localhost:5000/metadata
```
```
{
  "CENTER_NAME": "EARTH",
  "OBJECT_ID": "1998-067-A",
  "OBJECT_NAME": "ISS",
  "REF_FRAME": "EME2000",
  "START_TIME": "2024-075T12:00:00.000Z",
  "STOP_TIME": "2024-090T12:00:00.000Z",
  "TIME_SYSTEM": "UTC"
}
```
Using the route "/epochs?limit=int&offset=int", the user can recieve a list of epochs of length "limit" that starts at the "offset". The default for offset is 0 and the default for limit is the lenth of the dataset, so when this command is run without query parameters, it will return the entire dataset in the form of a list of epochs. Here is an example of the expected output for limit = 2, and offset = 1.

```
curl "localhost:5000/epochs?limit=2&offset=1"
```
```
[
  {
    "EPOCH": "2024-075T12:04:00.000Z",
    "X": {
      "#text": "-4893.8238680509903",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "-1.19130674008412",
      "@units": "km/s"
    },
    "Y": {
      "#text": "-1233.18749043554",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "-6.8853449488571803",
      "@units": "km/s"
    },
    "Z": {
      "#text": "4549.8950247933299",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "-3.1367876699428199",
      "@units": "km/s"
    }
  },
  {
    "EPOCH": "2024-075T12:08:00.000Z",
    "X": {
      "#text": "-4998.5872791117999",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "0.32368228959634998",
      "@units": "km/s"
    },
    "Y": {
      "#text": "-2820.8454591355598",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "-6.2644494579024697",
      "@units": "km/s"
    },
    "Z": {
      "#text": "3640.56209437198",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "-4.3947349595401803",
      "@units": "km/s"
    }
  }
]
```

The route "/epochs/(epoch)" will return the state vectors for a specific epoch. The epoch must be in the following format:
```
<year>-<day out of 365>T<hour>:<min>:<second>.<milliseconds>Z
```
Not every timestamp is available to be used as an epoch, it must be one that is already in the data. For example, if you wanted to find data for March 16th, 2024 at 12:08 a.m., you would use the following command:
```
curl localhost:5000/epochs/2024-075T12:08:00.000Z
```
```
{
  "EPOCH": "2024-075T12:08:00.000Z",
  "X": {
    "#text": "-4998.5872791117999",
    "@units": "km"
  },
  "X_DOT": {
    "#text": "0.32368228959634998",
    "@units": "km/s"
  },
  "Y": {
    "#text": "-2820.8454591355598",
    "@units": "km"
  },
  "Y_DOT": {
    "#text": "-6.2644494579024697",
    "@units": "km/s"
  },
  "Z": {
    "#text": "3640.56209437198",
    "@units": "km"
  },
  "Z_DOT": {
    "#text": "-4.3947349595401803",
    "@units": "km/s"
  }
}
```
The coordinates "X", "Y", and "Z" are in the J2000 reference frame, and the timestamp is in UTC time. "X_DOT", "Y_DOT", and "Z_DOT" represent the instantaneous velocity in each direction at that time.

The route "/epochs/(epoch)/speed" will return the speed for the given epoch in km/s. For example:
```
curl localhost:5000/epochs/2024-075T12:08:00.000Z/speed
```
```
{
  "epoch": "2024-075T12:08:00.000Z",
  "speed": 7.659098680642358
}
```

The route "/epochs/(epoch)/location" will return the location for the given epoch in the form of latitude, longitude, altitude, and geoposition. The latitude and longitude is written in decimal degrees, and the geoposition will tell you the nearest suburb or village it is above. For example:
```
curl localhost:5000/epochs/2024-077T21:44:00.000Z
```
```
{
  "altitude": 427.7898508843109,
  "geoposition": "Nanutarra, Shire Of Ashburton, Western Australia, Australia",
  "latitude": -22.789323399773004,
  "longitude": 115.47786117809547
}
```
If the ISS is over the ocean, the geoposition will say "No data, perhaps over an ocean". For example:
```
{
  "altitude": 424.79661884721963,
  "geoposition": "No data, perhaps over an ocean",
  "latitude": 32.43149854748942,
  "longitude": -144.62845332002348
}
```

Finally, the route "/now" will return the location dictionary and the instantaneous speed for the epoch that is nearest to the time when the function is run. For example, if I run this code on March 18th at 4:43 pm CT:
```
curl localhost:5000/now
```
```
{
  "epoch": "2024-077T21:44:00.000Z",
  "location": {
    "altitude": 427.7898508843109,
    "geoposition": "Nanutarra, Shire Of Ashburton, Western Australia, Australia",
    "latitude": -22.789323399773004,
    "longitude": 115.47786117809547
  },
  "speed": 7.653789715924686
}
```

## Running Containerized Unit Tests

Unit tests are used to check if the functions work properly. They are used for debugging, not for the actual program. In order to run unit tests, the container must be running in the background still. Then you can use the following command to run the tests:

```
python3 test/test_iss_tracker.py
```

## Citations

(1) NASA (2024) ISS Trajectory Data. Nasa's Spot the Station. [https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml](https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml)
