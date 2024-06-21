from scrapper_tiktok import scrapeVideos
from make_compilation import makeCompilation
from upload_ytvid import uploadYtvid
import schedule
import time
import datetime
import os
import shutil
from googleapiclient.discovery import build #pip install google-api-python-client
from google_auth_oauthlib.flow import InstalledAppFlow #pip install google-auth-oauthlib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

num_to_month = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "June",
    7: "July",
    8: "Aug",
    9: "Sept",
    10: "Oct",
    11: "Nov",
    12: "Dec"
} 

title = "BEST TIKTOK SKATEBOARDING COMPILATION - SKATECLIPZ AROUND THE WORLD"
now = datetime.datetime.now()
videoDirectory = "./Sktclipz_" + num_to_month[now.month].upper() + "_" + str(now.year) + "_V" + str(now.day) + "/"
outputFile = "./" + num_to_month[now.month].upper() + "_" + str(now.year) + "_v" + str(now.day) + ".mp4"

INTRO_VID = ''                 # PATH FOR YOUR INTRO VIDEO
OUTRO_VID = ''                 # PATH FOR YOUR OUTRO VIDEO
TOTAL_VID_LENGTH = 10*60       # MAX VIDEO LENGTH (10 min)
MAX_CLIP_LENGTH = 19           # MAX NUM OF CLIPS COMPILATED
MIN_CLIP_LENGTH = 5            # MIN NUM OF CLIPS COMPILATED
DAILY_SCHEDULED_TIME = "11:30" # HOUR OF THE DAY TO START EXECUTING
TOKEN_NAME = "token.json"      # Don't change / TOKEN CREATED BY GOOGLE API

# Setup Google 
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
client_secrets_file = "secret.json"

def routine():

    # Handle GoogleAPI oauthStuff
    print("Handling GoogleAPI")
    creds = None
    # The file token1.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_NAME):
        creds = Credentials.from_authorized_user_file(TOKEN_NAME, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_NAME, 'w') as token:
            token.write(creds.to_json())

    googleAPI = build('youtube', 'v3', credentials=creds)

    now = datetime.datetime.now()
    print(now.year, now.month, now.day, now.hour, now.minute, now.second)

    description = ""
    print(outputFile)

    if not os.path.exists(videoDirectory):
        os.makedirs(videoDirectory)
    
    # Step 1: Scrape Videos if not scraped yet
    lst = os.listdir(videoDirectory)
    if(len(lst) < 20):
        print("Scraping Videos...")
        scrapeVideos(output_folder = videoDirectory)
        print("Scraped Videos!")
    
    # Description stuff
    description = "Enjoy the clips! :) \n\n" \
    "like and subscribe to @atwskateclipz for more \n\n" \
    "if you want (or doesn't want) your clips to appear in this channel contact me at: andregehgoncalvesz@gmail.com \n\n" \

    # Step 2: Make Compilation
    print("Making Compilation...")
    description += makeCompilation(path = videoDirectory,
                    introName = INTRO_VID,
                    outroName = OUTRO_VID,
                    totalVidLength = TOTAL_VID_LENGTH,
                    maxClipLength = MAX_CLIP_LENGTH,
                    minClipLength = MIN_CLIP_LENGTH,
                    outputFile = outputFile)
    print(description)
    print("Made Compilation!")

    # Step 3: Upload to Youtube
    print("Uploading to Youtube...")
    uploadYtvid(VIDEO_FILE_NAME=outputFile,
                title=title,
                description=description,
                googleAPI=googleAPI)
    print("Uploaded To Youtube!")
    
    # Step 4: Cleanup
    print("Removing temp files!")
    # Delete all files made:
    shutil.rmtree(videoDirectory, ignore_errors=True)
    try:
        os.remove(outputFile)
    except OSError as e:  ## if failed, report it back to the user ##
        print ("Error: %s - %s." % (e.filename, e.strerror))
    print("Removed temp files!")

def attemptRoutine():
    while(1):
        try:
            routine()
            break
        except OSError as err:
            print("Routine Failed on " + "OS error: {0}".format(err))
            time.sleep(60*60)

# RUNS THE ROUTINE EVERY DAY
schedule.every().day.at(DAILY_SCHEDULED_TIME).do(attemptRoutine)

attemptRoutine()
while True:
    schedule.run_pending()  
    time.sleep(60) # wait one min

