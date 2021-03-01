from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
from pprint import pprint
from googleapiclient import discovery
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# here enter the id of your google sheet
SAMPLE_SPREADSHEET_ID_input = '1YylnFnVCNtkFOFEz0qg9PaBHwC1LEdRcGMGBVwe4INk'
SAMPLE_RANGE_NAME = 'Sheet1!A1:AA1000' #change this for other sheets

def getService():
    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_269040863650-4gmq13ovr1c8fsmlgnkqjmlc43f3rgct.apps.googleusercontent.com.json', SCOPES) # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

def readFromSheet(SHEET_ID = '17RJFfKeIfyupURzDaCyQ9rZbkR8JgJSl0c8-RMKBbwg', RANGE = 'A1:AA1000'):
    getService()

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID,
                                range=RANGE).execute()
    values = result.get('values', [])

    if not values:
        print('[ERROR]No data found.')
        return []
    else:
        print('[LOG]Fetched data from Google Sheets API.')
        return values

def writeToSheet(SHEET_ID= '1YylnFnVCNtkFOFEz0qg9PaBHwC1LEdRcGMGBVwe4INk', SAMPLE_RANGE_NAME = 'A1:AA1000', body = [['hello'], ['hello']] ):
    getService()

    # Call the Sheets API
    value_input_option = 'RAW'  # TODO: Update placeholder value.

    # clear the sheet 
    request = service.spreadsheets().values().clear(spreadsheetId=SHEET_ID, range=SAMPLE_RANGE_NAME, body={})
    response = request.execute()

    #update the sheet
    request = service.spreadsheets().values().update(spreadsheetId=SHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption=value_input_option, body=body)
    response = request.execute()
    print("[LOG]Update request to Google Sheets API: " + str(response))

# readFromSheet()
# writeToSheet()


