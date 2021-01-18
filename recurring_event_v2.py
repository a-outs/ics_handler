from icalendar import Calendar
import datetime
from import_export import get_calendar, make_output


def make_recurring(calendar):
    hash_by_name = create_hash(calendar)
    updated_cal = copy_start_cal(calendar)
    for name in hash_by_name:
        add_to_cal(updated_cal, hash_by_name[name])
    return updated_cal


def create_hash(calendar):
    event_names = {}
    for cur_event in calendar.walk('vevent'):
        if cur_event['summary'] not in event_names:
            event_names[cur_event['summary']] = [[cur_event, [(cur_event.get('dtstart')).dt]]]
        else:
            seven_days = datetime.timedelta(days=7)
            event_list = event_names[cur_event['summary']]
            test = 0
            for i in range(len(event_list)):
                if (((cur_event.get('dtstart')).dt - (
                        event_list[i][0].get('dtstart')).dt) % seven_days == datetime.timedelta(seconds=0)):
                    event_list[i][1].append((cur_event.get('dtstart')).dt)
                    test = 1
                    break
            if test == 0:
                event_list.append([cur_event, [(cur_event.get('dtstart')).dt]])
    return event_names


def copy_start_cal(calendar):
    new_cal = Calendar()
    new_cal.add('version', calendar['version'].to_ical())
    new_cal.add('prodid', calendar['prodid'].to_ical())
    new_cal.add('calscale', calendar['calscale'].to_ical())
    new_cal.add('method', calendar['method'].to_ical())
    return new_cal


def add_to_cal(calendar, event_occur_list):
    for i in range(len(event_occur_list)):
        day = (event_occur_list[i][0].get('dtstart')).dt.strftime("%a")
        day = day[: -1]
        exdates = get_exdates(event_occur_list[i][1])
        event_occur_list[i][0].add('rrule',
                                   {'freq': 'weekly', 'wkst': 'su', 'byday': day, 'count': len(event_occur_list[i][1]) + len(exdates)})
        event_occur_list[i][0].add('exdate', exdates)
        calendar.add_component(event_occur_list[i][0])


def get_exdates(datetime_list):
    exdate_list = []
    datetime_list.sort()
    for i in range(len(datetime_list) - 1):
        if datetime_list[i] - datetime_list[i + 1] != datetime.timedelta(days=-7):
            date = datetime_list[i] + datetime.timedelta(days=7)
            exdate_list.append(date)
    return exdate_list



cal = get_calendar("https://canvas.ucdavis.edu/feeds/calendars/user_ODFFhjDBOCcHqFYiZlS2riPi4WaYGAwHTQUbhraK.ics")
recur_cal = make_recurring(cal)
make_output(recur_cal, "test.ics")