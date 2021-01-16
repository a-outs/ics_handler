from icalendar import Calendar, Event
import urllib.request

def get_calendar():
    url_home = urllib.request.urlopen('https://canvas.ucdavis.edu/feeds/calendars/user_URNeG1MSEjHo2ChpoCUFan9VQ4NDe15UE3bzMlhj.ics').read()
    
    return url_home

def exclude_all_events(file):
    file_in_text = Calendar.from_ical(file)

    cal = Calendar()
    for old_event in file_in_text.walk('VEVENT'):
        uid = old_event.get('uid')
        event_string = 'event-calendar-event'

        if event_string not in uid:
            event = Event()

            summary = old_event.get('summary')
            dt_stamp = old_event.get('dtstamp').to_ical()
            start_date = old_event.get('dtstart').to_ical()
            end_date = old_event.get('dtend').to_ical()
            uid = old_event.get('uid')

            event['DTSTAMP'] = dt_stamp
            event['UID'] = uid
            event['DTSTART'] = start_date
            event['DTEND'] = end_date
            event['SUMMARY'] = summary

            cal.add_component(event)

    return cal

def blacklist_events(file, blacklist):
    file_in_text = Calendar.from_ical(file)

    cal = Calendar()
    for old_event in file_in_text.walk('VEVENT'):
        summary = old_event.get('summary')
        if (blacklist not in summary):
            event = Event()

            dt_stamp = old_event.get('dtstamp').to_ical()
            start_date = old_event.get('dtstart').to_ical()
            end_date = old_event.get('dtend').to_ical()
            uid = old_event.get('uid')

            event['DTSTAMP'] = dt_stamp
            event['UID'] = uid
            event['DTSTART'] = start_date
            event['DTEND'] = end_date
            event['SUMMARY'] = summary

            cal.add_component(event)
        
    return cal

file = get_calendar()
#calendar = blacklist_events(file, "Lecture")

calendar = exclude_all_events(file)

f = open('test1.ics', 'wb')
f.write(calendar.to_ical())
f.close()


