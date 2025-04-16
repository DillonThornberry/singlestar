import gspread
from oauth2client.service_account import ServiceAccountCredentials
import socketio
import json

# Connect to the Flask Socket.IO server at localhost:6464
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server!")

@sio.event
def disconnect():
    print("Disconnected from server!")

@sio.event
def connect_error(data):
    print("Failed to connect to server:", data)

def secToTime(seconds):
    """Convert seconds to a formatted string of minutes and seconds."""
    minutes = int(seconds) // 60
    seconds = float(seconds) % 60
    return f"{minutes:02}:{seconds:02}"

def timeToSec(time):
    
    """Convert a formatted string of minutes and seconds to total seconds."""
    if ":" in time:
        minutes, seconds = map(float, time.split(":"))
        return minutes * 60 + seconds
    else:
        return float(time)

def getSheet():
# Set up the credentials and client
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("key.json", scope)
    client = gspread.authorize(creds)

    # Open the sheet by name
    sheet = client.open("Star Times").sheet1  # or .worksheet("Sheet2")

    # Get all values
    data = sheet.get_all_records()

    name = None
    column = None

    players = sheet.row_values(1)[2:9]  # Get the player names from the first row
    print(players)

    while True:
        column = input("Enter column of your name (e.g. 'C', 'D', 'E', etc.): ")
        name = sheet.acell(column + "1").value  # Get the name from the first row of the specified column
        response = input(f"You are {name}? (y/n): ").strip().lower()
        if response == 'y':
            break
        elif response == 'n':
            print("\nPlease enter the correct column.")
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    while True:

        starNames = sheet.col_values(2)[2:118]  # Get all star names from column B, excluding the header
        for i in range(len(starNames)):
            print(f"{i+3}. {starNames[i]}")

        row = input("Enter row of star you are attempting (e.g. '2', '3', '4', etc.): ")
        star = sheet.acell('B' + row).value  # Get the star name from column B of the specified row

        


        print(f"Attempting: {star}")
        time = sheet.acell(column + row).value
        if time:
            time = secToTime(float(time))
        print(f"Your time: {time}")

        times = sheet.row_values(int(row))[2:9]
        #print(times)
        playertimes = [(players[i], times[i]) for i in range(len(times))]
        #print(playertimes)
        sorted_times = sorted(playertimes, key=lambda x: timeToSec(x[1]) if x[1] != '' else float('inf'))

        message = {"star": star, "me": name, "times": sorted_times}
        #print(sorted_times)

        sio.emit("update_message", {"message": json.dumps(message)})
        input("Press Enter to change star")


if __name__ == "__main__":
    sio.connect("http://localhost:6464")
    getSheet()
    sio.disconnect()
        
