# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/google-apps/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.

import datetime
import sys



def build_event_l(one_meal_list, start_time_in, start_date):
    '''
    example start_date: [2016,3,18]
    example start_time: [8,0,0]   i.e. 8:00:00
    '''
    year, month, day = start_date
    hour, minute, secend = start_time_in
    start_datetime = datetime.datetime(year, month, day, hour, minute, second)
    end_datetime = start_datetime + datetime.timedelta(hours = 2)
    rv_event_l = []
    for meal in one_meal_list:
        event = {}    
        event["summary"] = meal["name"]
        event["description"] = "calories: " + meal["calories"] + "    cooking time: " + meal["cooking_time"]
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


def syn_to_calendar(start_date):
    '''
    start_date example: [2016,3,10]
    '''
    with open("final_output.json") as f:
        result = json.load(f)
        breakfast_list = result["breakfast_final_list"]
        lunch_list = result["lunch_list"]
        dinner_list = result["dinner_list"]
        calories_list = result["calories_list"]
        alternative_breakfast_list = result["alternative_breakfast_list"]
        alternative_lunch_list = result["alternative_lunch_list"]
        alternative_dinner_list = result["alternative_dinner_list"]

    breakfast_events = build_event_l(breakfast_list, [8,0,0], start_date)
    lunch_events = build_event_l(lunch_list, [11,30,0], start_date)
    dinner_events = build_event_l(dinner_list, [17,0,0], start_date)

    for event in breakfast_events + lunch_events + dinner_events:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print 'Event created: %s' % (event.get('htmlLink'))


if __name__=="__main__":
    
    args = [sys.argv[1], sys.argv[2], sys.argv[3]]
    syn_to_calendar(args)

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









