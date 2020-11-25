import pickle
from datetime import datetime, timedelta

from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

import mypath

file_token = mypath.data_folder / "token.pkl"

scopes = ['https://www.googleapis.com/auth/calendar']


def get_next_match():
    now = get_current_time()

    # -6hours from current time due to some error w/gcalendar getting the wrong event
    now_minus = now - timedelta(hours=6)

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

    return next_match_summary, next_match_time, match_start_datetime, now_formatted


def compare_time():
    current_time = get_current_time()
    match = get_next_match()
    match_time = match[2]
    match_time = match_time.replace(tzinfo=None)

    # current_time = datetime(2020, 11, 8, 16, 50, 1)
    # match_time = datetime(2020, 11, 25, 21, 00, 0)
    difference = current_time - match_time
    difference = difference.total_seconds()
    # print('current time:', current_time)
    # print('match time: ', match[1])
    # print(difference)

    if difference >= -3601 and difference <= 0:
        return True
    else:
        return False


def get_current_time():
    now = datetime.now()
    return now


# if __name__ == "__main__":
#     compare_time()
