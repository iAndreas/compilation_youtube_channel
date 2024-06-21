from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

def downloadVideo(link, id, videoDirectory):
    print(f"Downloading video {id} from: {link}")

    cookies = {
        '_gid': 'GA1.2.2012770266.1698184111',
        '_gat_UA-3524196-6': '1',
        '_ga': 'GA1.2.1194048366.1698184111',
        '_ga_ZSF3D6YSLC': 'GS1.1.1698184110.1.0.1698184132.0.0.0',
    }

    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '_gid=GA1.2.2012770266.1698184111; _gat_UA-3524196-6=1; _ga=GA1.2.1194048366.1698184111; _ga_ZSF3D6YSLC=GS1.1.1698184110.1.0.1698184132.0.0.0',
        'hx-current-url': 'https://ssstik.io/en',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/en',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': '',
    }
    
    print("STEP 4: Getting the download link")
    print("If this step fails, PLEASE read the steps above")
    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")

    downloadLink = downloadSoup.a["href"]
    videoTitle = downloadSoup.p.getText().strip()

    print("STEP 5: Saving the video :)")
    mp4File = urlopen(downloadLink)
    username = (link.split('/'))[3]
    with open(f"{videoDirectory}{id}-{username}-{videoTitle}.mp4", "wb") as output:
        while True:
            data = mp4File.read(4096)
            if data:
                output.write(data)
            else:
                break

def scrapeVideos(output_folder):
    tiktokLink = "https://www.tiktok.com/search?q=skateboard" # Change to the link you want to extract content
    videoDirectory = output_folder # Change to where you want to keep your videos 
    print("STEP 1: Open Chrome browser")
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)

    driver.get(tiktokLink)

    # If you get a tiktok CAPTCHA, change the timeout here
    # to 60 seconds, just enough time for you to complete the captcha yourself.
    time.sleep(1)

    scroll_pause_time = 1
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1

    print("STEP 2: Scrolling page")
    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        if (screen_height) * i > scroll_height:
            break 

    script  = "let l = [];"
    script += "document.querySelectorAll(\""
    script += "div[aria-label='Assistir em tela cheia']"
    script += "\").forEach(item => {for(const child of item.children) {for(const child2 of child.children) { l.push(child2.querySelector('a').href)}}});"
    script += "return l;"
    time.sleep(10)

    urlsToDownload = driver.execute_script(script)

    print(f"STEP 3: Time to download {len(urlsToDownload)} videos")
    for index, url in enumerate(urlsToDownload):
        print(f"Downloading video: {index}")
        downloadVideo(url, index, videoDirectory)
        time.sleep(10)

if __name__ == "__main__":
    scrapeVideos(output_folder = "./videos")