# 🤖 Automated Compilation Youtube Channel 🤖

Start a fully automated youtube that can scrape content on tiktok, edit a compilation, and upload to youtube daily.

# 📝 How to Use 📝

1. Clone this Repository

2. Download and install [Python3](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/) if necessary.

3. Install the required libraries with `pip3 install -r requirements.txt` or `python3 -m pip install -r requirements.txt` .

4. Create a Project with the Youtube API: https://developers.google.com/youtube/v3/quickstart/python
Be sure to follow the instructions carefully, as it won't work if you don't do this right.
Download your OATH file and name it as "googleAPI.json" in the main project folder.

5. Run `python3 main.py` in your computer terminal (terminal or cmd). You have to sign in to your Youtube Account through the tab opened by the script. If a new tab doesn't open, copy the link generated in the script, paste it in your browser, and then sign into your Google account. Then paste the authentication code you get back into your terminal. It will then say "Starting Scraping" if it all goes ok.

6. Enjoy your new automated compilation youtube channel! :) 

NOTE: for uploading public videos, you have to complete an audit for the Youtube API. See the note in the [Google Documentation](https://developers.google.com/youtube/v3/docs/videos/insert). Without this, you can only post private videos, but the approving process is very simple.
