import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import datetime

def connect_gspread(jsonf,key):
  scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
  credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
  gc = gspread.authorize(credentials)
  worksheet = gc.open_by_key(key).sheet1
  return worksheet
  
def connect_google_calendar(jsonf):
  credentials = Credentials.from_service_account_file(jsonf)
  calendar = build('calendar', 'v3', credentials=credentials)
  return calendar

def get_schedule(data, summaryPrefix):
  schedule = []
  year = '2025'
  for row in range(1,len(data)):
    # 2025年のみ抽出
    if data[row][0] == '↑' + year + '年':
      return schedule

    # 「MM/dd」で始まる行のみ抽出
    pattern = '^(0[1-9]|1[0-2])\/(0[1-9]|[12][0-9]|3[01]).*$'
    if not re.match(pattern, data[row][0]):
      continue

    date_pattern = '^(0[1-9]|1[0-2])\/(0[1-9]|[12][0-9]|3[01])'

    date = year + '/' + re.match(date_pattern, data[row][0]).group()
    start_time = data[row][1]
    end_time = data[row][2]
    summary = summaryPrefix + data[row][3]
    location = data[row][4]
    station = '最寄駅: ' + data[row][5]
    if not date or not start_time or not end_time or not summary or not location or not station:
      continue

    start = datetime.datetime.strptime(date + ' ' + start_time, '%Y/%m/%d %H:%M')
    end = datetime.datetime.strptime(date + ' ' + end_time, '%Y/%m/%d %H:%M')
    
    # 辞書を構築してscheduleに格納
    schedule.append({
      'summary': summary,
      'location': location,
      'description': station,
      'start': {
        'dateTime': start.strftime('%Y-%m-%dT%H:%M:%S'),
        'timeZone': 'Asia/Tokyo',
      },
      'end': {
        'dateTime': end.strftime('%Y-%m-%dT%H:%M:%S'),
        'timeZone': 'Asia/Tokyo',
      },
      })
    
def delete_events(calendar, calendarId, summaryPrefix):
  today = datetime.datetime.utcnow().isoformat() + 'Z'
  events_result = calendar.events().list(
    calendarId=calendarId, 
    singleEvents=True,
    orderBy='startTime',
    timeMin=today
    ).execute()
  events = events_result.get('items', [])

  # summaryがsummaryPrefixで始まるイベントを一括削除
  batch = calendar.new_batch_http_request()
  deleted_count = 0
  for event in events:
    if event['summary'].startswith(summaryPrefix):
      # print(event['summary'])
      batch.add(calendar.events().delete(calendarId=calendarId, eventId=event['id']))
      deleted_count += 1
  batch.execute()
  print("LPP events deleted: %d" % deleted_count)
    
def register_event(calendar, schedule, calendarId):
  def callback(request_id, response, exception):
    if exception is not None:
      print(exception)
    else:
      print("Event created: %s" % response.get('htmlLink'))
  batch = calendar.new_batch_http_request(callback=callback)
  for event in schedule:
    batch.add(calendar.events().insert(calendarId=calendarId, body=event))
  batch.execute()

def main():
  jsonf = '/root/credentials/schedule-coordination-ff9219425143.json'
  spread_sheet_key = '1BHU5xZGcGugcypEGQH9wKF0IiFyJEbfvoSOhfMtaHwg'
  calendarId = 'c3a446e445fd0b159f9ba67960388269ed3815e731cd256c4cc842ba079dec39@group.calendar.google.com'
  summaryPrefix = 'LPP:'

  worksheet = connect_gspread(jsonf, spread_sheet_key)
  data = worksheet.get_all_values()
  schedule = get_schedule(data, summaryPrefix)

  calendar = connect_google_calendar(jsonf)
  delete_events(calendar, calendarId, summaryPrefix)
  register_event(calendar, schedule, calendarId)

if __name__ == '__main__':
  main()
