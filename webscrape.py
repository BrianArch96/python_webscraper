import requests
from lecture import Lecture
from timetable import Timetable
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

STUDENT_ID = '15168867'
def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    payload = {'T1': STUDENT_ID}
    session = requests.Session()
    try:
        result = session.post(url, data=payload)
    except RequestException as e:
        log_error('Did not work')
        return "Error"
    timetable = parse(result.text)
    print(timetable.monday[0].module)
    return "Success"

def is_good_response(resp):
   
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def parse(timetable_html):

    soup = BeautifulSoup(timetable_html, 'html.parser')
    results = soup.find_all('td', attrs={'valign':'top'})
    days = []
    for day in results:
        days.append(parse_days(day))
    timetable = Timetable(days[0], days[1], days[2], days[3], days[4], days[5])
    return timetable

def parse_days(day):

    lectures = day.find_all('font', attrs={'size':'1'})
    daily_lectures = []
    for lecture in lectures:
        lecture_raw = lecture.find('b').get_text()
        newstr = lecture_raw.replace('-','')
        attrs = newstr.split()
        if (str(attrs[3]) == 'LAB') or (str(attrs[3]) == 'TUT'):
            attrs[3] = attrs[3] + '-' + attrs[4]
            attrs[4] = attrs[5]
        lecture_attr = Lecture(attrs[0], attrs[1], attrs[2], attrs[3], attrs[4])
        daily_lectures.append(lecture_attr)
    return daily_lectures

def log_error(e):

    print(e)
