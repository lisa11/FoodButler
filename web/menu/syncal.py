# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/google-apps/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.


def syn_one_meal(one_meal_list, start_time, end_time, start_date, reminders = False):
    event = {}
    
    for meal in one_meal_list:
        event["summary"] = meal["name"]
        event["description"] = "calories: " + meal["calories"] + "    cooking time: " + meal["cooking_time"]
        event["start"] = {"dateTime": start_time, "timeZone": "America/Chicago"}
        event["end"] = {"dateTime": end_time, "timeZone": "America/Chicago"}
        event['reminders'] = {'useDefault': reminders, 'overrides': [{'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},]}
    return event


def syn_to_calendar(start_date):

    with open("final_output.txt") as f:
        breakfast_list, lunch_list, dinner_list, calories_list, alternative_breakfast_list, alternative_lunch_list, alternative_dinner_list = f.readline()
    bre

event = {
  'summary': 'Google I/O 2015',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2015-05-28T09:00:00-06:00',
    'timeZone': 'America/Chicago',
  },
  'end': {
    'dateTime': '2015-05-28T17:00:00-06:00',
    'timeZone': 'America/Chicago',
  },
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

event = service.events().insert(calendarId='primary', body=event).execute()
print 'Event created: %s' % (event.get('htmlLink'))


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