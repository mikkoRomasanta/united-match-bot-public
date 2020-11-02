import pickle
from datetime import datetime, timedelta

from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

import mypath

file_token = mypath.data_folder / "token.pkl"

scopes = ['https://www.googleapis.com/auth/calendar']


def get_next_match():
    now = get_current_time
    # -12hours from current time due to some error w/gcalendar getting the wrong event
    now_minus = datetime.now() - timedelta(hours=12)
    now_formatted = now_minus.isoformat() + 'Z'
    credentials = pickle.load(
        open(file_token, "rb"))
    service = build("calendar", "v3", credentials=credentials)
    result = service.calendarList().list().execute()  # get all calendars
    # 2 = mutd matches calendar
    calendar_id = result['items'][2]['id']
    result = service.events().list(calendarId=calendar_id, timeMin=now_formatted, maxResults=3, timeZone="Asia/Manila",
                                   singleEvents=True, orderBy="startTime").execute()  # get next match
    next_match_summary = result['items'][0]['summary']

    match_start = result['items'][0]['start']['dateTime']
    match_start_formatted = datetime.fromisoformat(
        match_start).ctime()  # more readable date format

    # will be used for start time display
    next_match_time = match_start_formatted

    match_start_datetime = datetime.strptime(
        match_start, "%Y-%m-%dT%H:%M:%S%z")  # will be used for datetime comparison

    return next_match_summary, next_match_time, match_start_datetime


def compare_time():
    current_time = get_current_time()
    match = get_next_match()
    match_time = match[2]
    match_time = match_time.replace(tzinfo=None)

    # current_time = datetime(2020, 11, 4, 23, 30, 0)
    # match_time = datetime(2020, 11, 5, 0, 30, 0)
    difference = current_time - match_time
    difference = difference.total_seconds()
    # print(current_time)
    # print(match_time)
    # print(difference)

    if difference >= -3601:
        return True
    else:
        return False


# def compare_time1():
#     current_time = get_current_time()
#     next_match = get_next_match()
#     next_match_time = next_match[2]

#     next_match_time2 = next_match_time.replace(tzinfo=None)

#     difference = current_time - next_match_time2
#     test = difference.total_seconds()
#     return test


def get_current_time():
    now = datetime.now()
    return now


if __name__ == "__main__":
    # next_match = get_next_match()
    # print(next_match[0])
    # print(next_match[1])
    # test = compare_time()
    # print(test)
    # print(get_current_time())
