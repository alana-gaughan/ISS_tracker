import requests
import xmltodict
from flask import Flask, request
from datetime import datetime
from math import sqrt

app = Flask(__name__)

@app.route('/epochs', methods=['GET'])
def find_iss_list():
    '''
    Outputs:
    response_list (list): This is a list of dicts that contains the data from the ISS tracker. The length of the list is the limit, and the list begins at the offset index
    '''
    list_of_keys = ['ndm', 'oem', 'body', 'segment', 'data', 'stateVector']
    response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    response_dict = xmltodict.parse(response.content)
    for key_string in list_of_keys:
        response_dict = response_dict[key_string]
    response_list = response_dict

    limit = request.args.get('limit', f"{len(response_list)}")
    offset = request.args.get('offset', '1')
    try:
        limit = int(limit)
    except ValueError:
        return "Error: limit must be a positive integer"
    try:
        offset = int(offset)
    except ValueError:
        return "Error: offset muct be a positive integer"
    return response_list[offset - 1 :limit + offset - 1]

def epoch_to_list(epoch_string):
    '''
    inputs:
    epoch_string (string): This is a string from a stateVector dictionary with "EPOCH" as the key

    outputs:
    epoch_list (list): This is list in the form of [year, day of year, hour, minute]
    '''
    epoch_date_time = epoch_string.split('T')
    epoch_year_day = epoch_date_time[0].split('-')
    epoch_hr_min = epoch_date_time[1].split(':')
    year = int(epoch_year_day[0])
    day = int(epoch_year_day[1])
    hour = int(epoch_hr_min[0])
    minute = int(epoch_hr_min[1])

    epoch_list = [year, day, hour, minute]
    return epoch_list

def find_closest_epoch(list_of_dicts, current_date_time):
    '''
    Inputs:
    list_of_dicts (list[dicts]): This is the list of ISS data that was pulled from NASA

    current_date_time (list[ints]): This is the current time found using python's datetime library in the form of [year, month, day, hour, minute, second]

    Outputs:
    current_epoch (dict): The dictionary from list_of_dicts with the time stamp that is closest to teh current time
    '''
    # Turn the current time into [year, day, hour, minute] format
    # turn month, day into day of year
    days_in_months = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    current_year = current_date_time[0]
    current_month = current_date_time[1]
    current_day = current_date_time[2]
    current_hour = current_date_time[3]
    current_minute = current_date_time[4]
    current_second = current_date_time[5]


    #don't forget about leap year
    leap_year = False
    if current_year % 4 == 0:
        if current_year % 100 == 0:
            if current_year % 400 == 0:
                leap_year = True
                for days in days_in_months[1:]:
                    days += 1
        else:
            leap_year = True
            for days in days_in_months[1:]:
                days += 1

    current_day += days_in_months[current_month - 1]
  
    # round to nearest min

    if current_second >= 30:
        current_minute += 1

    # if min = 60, change the hour
    if current_minute == 60:
        current_hour += 1
        current_minute = 0

    # if hour = 24, change the day
    if current_hour == 24:
        current_hour = 0
        current_day += 1

    # if day > 365, change the day to 1 unless it's a leap year
    if (current_day > 365 and leap_year == False) or (current_day > 366 and leap_year == True):
        current_day = 1
        
    current_time_in_min = current_day*(24*60) + current_hour*60 + current_minute
    
    closest_epoch = dict()
    # loop through list of dicts until it matches
    index = 1
    for iss_dict in list_of_dicts:
        # print(epoch_to_list(iss_dict['EPOCH']))
        epoch_list = epoch_to_list(iss_dict['EPOCH'])
        epoch_time_in_min = epoch_list[1]*(24*60) + epoch_list[2]*60 + epoch_list[3]
        #final part of function
        if abs(epoch_time_in_min - current_time_in_min) < 2:
            closest_epoch = iss_dict
        elif abs(epoch_time_in_min - current_time_in_min) == 2:
            if current_second < 30:
                closest_epoch = iss_dict
                break
            else:
                closest_epoch = list_of_dicts[index]
                break
        index += 1

    return closest_epoch

@app.route('/epochs/<epoch>', methods=['GET'])
def find_matching_epoch(epoch):
    '''
    Inputs:
    epoch (str): This is the string of the time stamp in the form <YEAR>-<DAY>T<HOUR>:<MINUTE>:<SECOND>.<MILISECOND>Z

    Outputs:
    iss_state_vector (dict): This is the dictionary of state vectors from the ISS data that matches the timestamp
    '''
    iss_list = find_iss_list()
    for iss_state_vector in iss_list:
        iss_epoch = iss_state_vector['EPOCH']
        if iss_epoch == epoch:
            return iss_state_vector
    return "Error: epoch is not in data set"

@app.route('/epochs/<epoch>/speed', methods=['GET'])
def find_matching_speed(epoch):
    '''
    Inputs:
    epoch (str): This is the string of the time stamp in the form <YEAR>-<DAY>T<HOUR>:<MINUTE>:<SECOND>.<MILISECOND>Z

    Outputs:
    return_dictionary (dict): This dictionary has the key epoch with the valuebeing the timestamp, and the key speed which has the value of the speed of the ISS at the time stamp

    '''
    match_epoch = find_matching_epoch(epoch)
    speed = calculate_current_speed(match_epoch)
    return_dictionary = {'epoch': epoch, 'speed' : speed}
    return return_dictionary

def calculate_current_speed(epoch_dict):
    '''
    Inputs:
    epoch_dict (dict): a dict of the current epoch
    
    Outputs:
    current speed (float): the speed of the iss from closest to when the program is run 
    '''
    x_dot = float(epoch_dict['X_DOT']['#text'])
    y_dot = float(epoch_dict['Y_DOT']['#text'])
    z_dot = float(epoch_dict['Z_DOT']['#text'])
    current_speed = sqrt( x_dot**2 + y_dot**2 + z_dot**2)
    return current_speed

@app.route('/now', methods=['GET'])
def find_now():
    '''
    Outputs:
    return_dictionary (dict): This dictionary has the key epoch with the valuebeing the timestamp of the time this function is called, and the key speed which has the value of the speed of the ISS at the current time
    '''
    current_date_time = datetime.now()
    current_date_time_list = [current_date_time.year, current_date_time.month, current_date_time.day, current_date_time.hour, current_date_time.minute, current_date_time.second]

    iss_list = find_iss_list()
    
    current_epoch = find_closest_epoch(iss_list, current_date_time_list)

    instant_speed = calculate_current_speed(current_epoch)
    
    return_dictionary = {'epoch' : current_epoch['EPOCH'], 'speed' : instant_speed}

    return return_dictionary

if __name__ == "__main__":
   app.run(debug=True, host = '0.0.0.0')
