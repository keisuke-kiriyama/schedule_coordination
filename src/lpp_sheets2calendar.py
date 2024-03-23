import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_gspread(jsonf,key):
    # 認証情報の設定
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)

    # SpreadSheetへの接続
    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_key(key).sheet1
    return worksheet
  
# SpreadSheetから取得したデータから予定を抽出する
def get_schedule(data):
  # 辞書型のスケジュールを格納するリストを定義する
  schedule = []
  year = '2024'
  for row in range(1,len(data)):
    # 2024年のみ抽出
    if data[row][0] == '↑' + year + '年':
      return schedule

    # 「MM/dd」で始まる行のみ抽出
    pattern = '^(0[1-9]|1[0-2])\/(0[1-9]|[12][0-9]|3[01]).*$'
    if not re.match(pattern, data[row][0]):
      continue

    date_pattern = '^(0[1-9]|1[0-2])\/(0[1-9]|[12][0-9]|3[01])'

    date = year + '/' + re.match(date_pattern, data[row][0]).group()
    start = data[row][1]
    end = data[row][2]
    title = 'LPP: ' + data[row][3]
    place = data[row][4]
    station = data[row][5]
    if not date or not start or not end or not title or not place or not station:
      continue

    
    # 辞書を構築してscheduleに格納
    schedule.append({
      'date': date,
      'start': start,
      'end': end,
      'title': title,
      'place': place,
      'station': station
      })
    
 
def main():
  jsonf = '/root/credentials/schedule-coordination-ff9219425143.json'
  spread_sheet_key = '1BHU5xZGcGugcypEGQH9wKF0IiFyJEbfvoSOhfMtaHwg'

  worksheet = connect_gspread(jsonf, spread_sheet_key)
  data = worksheet.get_all_values()
  schedule = get_schedule(data)
  print(schedule)

if __name__ == '__main__':
  main()
