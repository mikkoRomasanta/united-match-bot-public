import pickle
from datetime import datetime

from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

scopes = ['https://www.googleapis.com/auth/calendar']

now = datetime.now()


def get_next_match():
    now_formatted = now.isoformat() + 'Z'
    credentials = pickle.load(open("token.pkl", "rb"))
    service = build("calendar", "v3", credentials=credentials)
    result = service.calendarList().list().execute()  # get all calendars
    # 2 = mutd matches calendar
    calendar_id = result['items'][2]['id']
    result = service.events().list(calendarId=calendar_id, timeMin=now_formatted, maxResults=1, timeZone="Asia/Manila",
                                   singleEvents=True, orderBy="startTime").execute()  # get next match

    next_match_summary = result['items'][0]['summary']

    match_start = result['items'][0]['start']['dateTime']
    match_start_formatted = datetime.fromisoformat(
        match_start).ctime()  # more readable date format

    next_match_time = match_start_formatted

    match_start_datetime = datetime.strptime(
        match_start, "%Y-%m-%dT%H:%M:%S%z")
    match_start_datetime = match_start_datetime.strftime(
        "%Y-%m-%d %H:%M:%S")

    return next_match_summary, next_match_time, match_start_datetime


def compare_time():
    next_match = get_next_match()
    next_match_time = next_match[2]
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    # print(next_match_time.hour)
    # print(current_time.hour)
    # print(next_match_time.hour)

    print(next_match_time)
    print(current_time)
    print(current_time - next_match_time)


if __name__ == "__main__":
    next_match = get_next_match()
    # print(next_match[0])
    # print(next_match[1])
    compare_time()
