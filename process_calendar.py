from icalendar import Calendar, Event
import urllib.request
import random

def get_calendar(url):
    ics_file = urllib.request.urlopen(url).read()
    return ics_file

def add_event_to_cal(old_event, cal):
    event = Event()

    summary = old_event.get('summary')
    dt_stamp = old_event.get('dtstamp').to_ical()
    start_date = old_event.get('dtstart').to_ical()
    end_date = old_event.get('dtend').to_ical()
    uid = old_event.get('uid')
    url = old_event.get('url')

    event['DTSTAMP'] = dt_stamp
    event['UID'] = uid
    event['DTSTART'] = start_date
    event['DTEND'] = end_date
    event['SUMMARY'] = summary
    event['URL'] = url

    cal.add_component(event)

def exclude_all_non_assignments(file):
    file_in_text = Calendar.from_ical(file)

    cal = Calendar()
    for old_event in file_in_text.walk('VEVENT'):
        uid = old_event.get('uid')
        event_string = 'event-calendar-event'

        if event_string not in uid:
            add_event_to_cal(old_event, cal)

    return cal.to_ical()

def blacklist_events(file, blacklist):
    file_in_text = Calendar.from_ical(file)

    cal = Calendar()
    for old_event in file_in_text.walk('VEVENT'):
        summary = old_event.get('summary')
        if (blacklist not in summary):
            add_event_to_cal(old_event, cal)
        
    return cal.to_ical()

def seperate_cal_by_course(file): 
    cal_dict = {}

    file_in_text = Calendar.from_ical(file)
    for event in file_in_text.walk('VEVENT'):
        course_url = event.get('url')
        # Course id is a 6 digit number followed by include_contexts=course_ in the url
        course_id = course_url.split("include_contexts=course_")
        course_id = course_id[1][:6]
        print(course_id)

        if course_id not in cal_dict:
            # Create a new calendar object for course id
            cal_dict[course_id] = Calendar()
            # Add that event to calendar
            add_event_to_cal(event, cal_dict[course_id])
        else:
            add_event_to_cal(event, cal_dict[course_id])
    
    return cal_dict

def generate_unique_number(list):
    name_num = random.randint(10000, 99999)
    if name_num not in list:
        return name_num
    else:
        generate_unique_number(list)

def write_file(name, calendar):
    f = open(name, 'wb')
    f.write(calendar)
    f.close()

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
        num_list = []
        name_list = []
        cal_dict = seperate_cal_by_course(file)

        for key in cal_dict:
            name_num = generate_unique_number(num_list)
            # Add the unique number to a list so it won't get repeated in the future
            num_list.append(name_num)

            # Write to file, and add the file names to a list that will be returned.
            file_name = str(name_num) + ".ics"
            name_list.append(file_name)
            write_file(file_name, cal_dict[key].to_ical())
        
        return name_list 

given_dict = {"inputLinkData":"https://canvas.ucdavis.edu/feeds/calendars/user_URNeG1MSEjHo2ChpoCUFan9VQ4NDe15UE3bzMlhj.ics","blacklistData":"MAT 021B","seperateData":True,"excludeEventsData":True}
filter_calendar(given_dict)



