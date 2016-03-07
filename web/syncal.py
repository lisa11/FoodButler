# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/google-apps/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

import json
import datetime
import sys


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'FoodButler'

BREAKFAST_START_TIME = [8,0,0]
LUNCH_START_TIME = [11,30,0]
DINNER_START_TIME = [17,0,0]


def build_event_l(one_meal_list, start_time_in, start_date):
    '''
    example start_date: [2016,3,18]
    example start_time: [8,0,0]   i.e. 8:00:00
    '''
    year, month, day = start_date
    hour, minute, second = start_time_in
    start_datetime = datetime.datetime(int(year), int(month), int(day), hour, minute, second)

    end_datetime = start_datetime + datetime.timedelta(hours = 2)
    rv_event_l = []
    for meal in one_meal_list:
        event = {}    
        event["summary"] = meal["name"]
        event["description"] = "calories: " + str(meal["calories"]) + "    cooking time: " + meal["cooking_time"]
        start_datetime_s = str(start_datetime)
        s_date, s_time = start_datetime_s.split()
        start_time = s_date + "T" + s_time + "-06:00"
        end_datetime = start_datetime + datetime.timedelta(hours = 2)
        end_time_s = str(end_datetime)
        e_date, e_time = end_time_s.split()
        end_time = e_date +  "T" + e_time + "-06:00"
        event["start"] = {"dateTime": start_time, "timeZone": "America/Chicago"}
        event["end"] = {"dateTime": end_time, "timeZone": "America/Chicago"}
        start_datetime = start_datetime + datetime.timedelta(days = 1)
        rv_event_l.append(event)
    return rv_event_l


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def syn_to_calendar(start_date):
    '''
    start_date example: [2016,3,10]
    '''
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    with open("final_output.json") as f:
        result = json.load(f)
        breakfast_list = result["breakfast_final_list"]
        lunch_list = result["lunch_list"]
        dinner_list = result["dinner_list"]

    breakfast_events = build_event_l(breakfast_list, BREAKFAST_START_TIME, start_date)
    lunch_events = build_event_l(lunch_list, LUNCH_START_TIME, start_date)
    dinner_events = build_event_l(dinner_list, DINNER_START_TIME, start_date)

    for event in breakfast_events + lunch_events + dinner_events:
        event = service.events().insert(calendarId='primary', body=event).execute()
        #print 'Event created: %s' % (event.get('htmlLink'))

syn_to_calendar([2016,3,10])

'''
def add_attachment(calendarService, driveService, calendarId, eventId, fileId):
    file = driveService.files().get(fileId=fileId).execute()
    event = calendarService.events().get(calendarId=calendarId,
                                         eventId=eventId).execute()

    attachments = event.get('attachments', []])
    attachments.append({
        'fileUrl': file['alternateLink'],
        'mimeType': file['mimeType'],
        'title': file['title']
    })

    changes = {
        'attachments': attachments
    }
    calendarService.events().patch(calendarId=calendarId, eventId=eventId,
                                   body=changes,
                                   supportsAttachments=True).execute()
'''









