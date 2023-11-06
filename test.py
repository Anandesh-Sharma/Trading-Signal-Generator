import json
import websocket
import threading
import requests
# Replace with your Fyers API credentials
api_key = 'HXUPRW6Q5Q-100'
api_secret = '10EUFXUX64'
access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTkyOTQ0NjIsImV4cCI6MTY5OTMxNzAyMiwibmJmIjoxNjk5Mjk0NDYyLCJhdWQiOlsiZDoxIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbFNTei1ZY29xbEljNGdfbHRZVW5EOW9QZGZLcE5ZQ0M4bk1NTVRIaDlHVWRsbzZieUZJWE1mSllUWlhPRl9PaktZUlotWlVwNVY5M0V0YUJ1TTB1c2dLWlEtTGxFX3o0U050SjF0SXZEbWxBNFFxST0iLCJkaXNwbGF5X25hbWUiOiJBTkFOREVTSCIsIm9tcyI6IksxIiwiaHNtX2tleSI6bnVsbCwiZnlfaWQiOiJYQTE5NTg1IiwiYXBwVHlwZSI6MTAwLCJwb2FfZmxhZyI6Ik4ifQ.s0H1Jz66vm_BlAp2aDEaExJddV7jkxi6M9n7GD0I7a0'

# Set the instrument token for the desired stock or index
instrument_token = 123456  # Replace with the instrument you want to track

# Define the WebSocket URL
ws_url = 'wss://realtime.fyers.in/socket.io/?EIO=3&transport=websocket'

# Fyers API endpoints
api_base_url = 'https://api.fyers.in/api/v2/'

# Function to authenticate and obtain a session token
def authenticate(api_key, api_secret):
    auth_payload = {
        'appID': api_key,
        'secret': api_secret
    }
    response = requests.post(api_base_url + 'get_token', data=auth_payload)
    return response.json()

# Function to subscribe to real-time data
def subscribe_to_realtime_data(access_token, instrument_token, callback):
    headers = {
        'authorization': f'Bearer {access_token}'
    }

    subscribe_payload = {
        'instrument_token': instrument_token
    }

    ws = websocket.WebSocketApp(ws_url, on_message=callback)
    ws.on_open = lambda ws: ws.send(json.dumps(subscribe_payload))
    ws.run_forever()

# Callback function to handle real-time data
def on_message(ws, message):
    data = json.loads(message)
    if 't' in data:
        timestamp = data['t']
        ohlc_data = data['d']

        # Example: Parse and print OHLC data
        print(f'Timestamp: {timestamp}, OHLC: {ohlc_data}')

# Authenticate and obtain the access token
auth_response = authenticate(api_key, api_secret)

if 'data' in auth_response and 'access_token' in auth_response['data']:
    access_token = auth_response['data']['access_token']
    print(f'Authenticated with access token: {access_token}')

    # Subscribe to real-time data
    subscribe_to_realtime_data(access_token, instrument_token, on_message)
else:
    print('Authentication failed. Please check your API credentials.')