from icalendar import Calendar, Event
import urllib.request
import random
import datetime

def get_calendar(url):
    ics_file = urllib.request.urlopen(url).read()
    return ics_file

def filter_by_case(original_cal, start_date, end_date): 
    if not start_date and not end_date:
        return original_cal

    elif start_date and not end_date:
        start_date = start_date.split("-")
        start = datetime.datetime(int(start_date[0]), int(start_date[1]), int(start_date[2])) 

        cal = Calendar()
        for old_event in original_cal.walk('VEVENT'):
            event_date = old_event.get("dtend").dt

            # Remove timezone info so the two dates can be compared
            if start <= event_date.replace(tzinfo=None):
                cal.add_component(old_event)
    
    elif not start_date and end_date:
        end_date = end_date.split("-")
        end = datetime.datetime(int(end_date[0]), int(end_date[1]), int(end_date[2]))

        cal = Calendar()
        for old_event in original_cal.walk('VEVENT'):
            event_date = old_event.get("dtend").dt

            # Remove timezone info so the two dates can be compared
            if event_date.replace(tzinfo=None) <= end:
                cal.add_component(old_event)
    
    else:
        start_date = start_date.split("-")
        end_date = end_date.split("-")
        start = datetime.datetime(int(start_date[0]), int(start_date[1]), int(start_date[2]))
        end = datetime.datetime(int(end_date[0]), int(end_date[1]), int(end_date[2]))

        cal = Calendar()
        for old_event in original_cal.walk('VEVENT'):
            event_date = old_event.get("dtend").dt
            
            # Remove timezone info so the two dates can be compared
            if start <= event_date.replace(tzinfo=None) <= end:
                cal.add_component(old_event)
    
    return cal.to_ical()

def filter_by_date(file, start_date, end_date):
    file_in_text = Calendar.from_ical(file)
    
    return filter_by_case(file_in_text, start_date, end_date)

def exclude_all_non_assignments(file):
    file_in_text = Calendar.from_ical(file)

    cal = Calendar()
    for old_event in file_in_text.walk('VEVENT'):
        uid = old_event.get('uid')
        event_string = 'event-calendar-event'

        if event_string not in uid:
            cal.add_component(old_event)

    return cal.to_ical()

def blacklist_events(file, blacklist):
    file_in_text = Calendar.from_ical(file)

    cal = Calendar()
    for old_event in file_in_text.walk('VEVENT'):
        summary = old_event.get('summary').lower()
        blacklist = blacklist.lower()
        if (blacklist not in summary):
            cal.add_component(old_event)
        
    return cal.to_ical()

def whitelist_events(file, whitelist):
    file_in_text = Calendar.from_ical(file)

    cal = Calendar()
    for old_event in file_in_text.walk('VEVENT'):
        summary = old_event.get('summary')
        if (whitelist in summary):
            cal.add_component(old_event)
        
    return cal.to_ical()

def seperate_cal_by_course(file): 
    cal_dict = {}

    file_in_text = Calendar.from_ical(file)
    for event in file_in_text.walk('VEVENT'):
        course_url = event.get('url')
        # Course id is a 6 digit number followed by include_contexts=course_ in the url
        course_id = course_url.split("include_contexts=course_")
        course_id = course_id[1][:6]

        if course_id not in cal_dict:
            # Create a new calendar object for course id
            cal_dict[course_id] = Calendar()
            # Add that event to calendar
            cal_dict[course_id].add_component(event)
        else:
            cal_dict[course_id].add_component(event)
    
    return cal_dict

def generate_unique_number(list):
    name_num = random.randint(10000, 99999)
    if name_num not in list:
        return name_num
    else:
        generate_unique_number(list)

def write_file(name, calendar):
    save_path = "../build/"
    name = save_path + name
    f = open(name, 'wb')
    f.write(calendar)
    f.close()

def filter_calendar(dict):
    input_link = dict["inputLinkData"]
    blacklist_terms = dict["blacklistData"]
    is_cal_separated = dict["separateData"]
    is_non_assignment_excluded = dict["excludeEventsData"]
    start_date = dict["startDate"]
    end_date = dict["endDate"]

    # Create unfiltered calendar
    file = get_calendar(input_link)

    # Remove events that are outside of the date range
    file = filter_by_date(file, start_date, end_date)

    # Take filtered list from prev. step and remove non assignments if specified
    if is_non_assignment_excluded:
        file = exclude_all_non_assignments(file)
    
    # Take filtered list from prev. step and filter with blacklist terms
    if blacklist_terms:
        blacklist_terms_in_list = blacklist_terms.split(", ")
        for term in blacklist_terms_in_list:
            file = blacklist_events(file, term)

    # Take the filtered list from prev. and see if it needs to be split into seperate calendars
    if is_cal_separated:
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
    else:
        num_list = []
        name_list = []
        name_num = generate_unique_number(num_list)
        file_name = str(name_num) + ".ics"

        write_file(file_name, file) 
        name_list.append(file_name)
        return name_list



