from icalendar import Calendar, Event
import urllib.request


def get_calendar(url):
    calendar = Calendar.from_ical(urllib.request.urlopen(url).read())
    return calendar


def make_output(calendar, filename):
    f = open(filename, "wb")
    f.write(calendar.to_ical())
    f.close()
