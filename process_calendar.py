from icalendar import Calendar, Event
import urllib.request
import json

def get_calendar(url):
    ics_file = urllib.request.urlopen(url).read()
    return ics_file

def exclude_all_non_assignments(file):
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

    return cal.to_ical()

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
        
    return cal.to_ical()

def seperate_cal_by_course(file): # returns list
    cal_dict = {}

    file_in_text = Calendar.from_ical(file)
    for event in file_in_text.walk('VEVENT'):
        course_url = event.get('url')
        print(course_url)
        '''
        course_id = course_url.split("include_contexts=course_")
        course_id = course_id[1][:7]
        print(course_id)
        '''

def filter_calendar(dict):
    input_link = dict["inputLinkData"]
    blacklist_terms = dict["blacklistData"]
    is_cal_seperated = dict["seperateData"]
    is_non_assignment_excluded = dict["excludeEventsData"]

    # Create unfiltered calendar
    file = get_calendar(input_link)

    # Remove non assignments if specified
    if is_non_assignment_excluded:
        file = exclude_all_non_assignments(file)
    
    # Take filtered list from prev. step and filter with blacklist terms
    if blacklist_terms:
        blacklist_terms_in_list = blacklist_terms.split(", ")
        for term in blacklist_terms_in_list:
            file = blacklist_events(file, term)

    # Take the filtered list from prev. and see if it needs to be split into seperate calendars
    if is_cal_seperated:
        seperate_cal_by_course(file)
    

    f = open('test4.ics', 'wb')
    f.write(file)
    f.close()

given_dict = {"inputLinkData":"https://canvas.ucdavis.edu/feeds/calendars/user_URNeG1MSEjHo2ChpoCUFan9VQ4NDe15UE3bzMlhj.ics","blacklistData":"MAT 021B","seperateData":True,"excludeEventsData":True}
filter_calendar(given_dict)

'''
file = get_calendar()
calendar = exclude_all_non_assignments(file)

f = open('test1.ics', 'wb')
f.write(calendar)
f.close()
'''


