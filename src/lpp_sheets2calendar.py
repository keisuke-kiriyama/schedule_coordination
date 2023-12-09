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
  
def main():
  jsonf = '/root/credentials/schedule-coordination-ff9219425143.json'
  spread_sheet_key = '1BHU5xZGcGugcypEGQH9wKF0IiFyJEbfvoSOhfMtaHwg'

  worksheet = connect_gspread(jsonf, spread_sheet_key)
  data = worksheet.get_all_values()
  print(data[35])

if __name__ == '__main__':
  main()
