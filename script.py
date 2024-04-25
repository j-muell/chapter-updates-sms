import configparser
import smtplib
import ssl
from email.message import EmailMessage
from bs4 import BeautifulSoup
import time
import urllib.request


# OPEN CONFIG FILE & SAVE VALUES
config = configparser.ConfigParser()
config.read('config.ini')

phoneNumber = config['sms']['phone_number']
smsGateWay = config['sms']['gateway']

sender = config['email']['sender']
senderPassword = config['email']['sender_password']

# CREATE EMAIL NUMBER WITH THE SMS GATEWAY AND PHONE NUMBER
emailNumber = phoneNumber + '@' + smsGateWay

# set the base url of your webnovel from webnovelworld.org
baseUrl = config['url']['base_url']
novelUrl = config['url']['novel_url']
pageNumber = 1
novelTitle = config['novel']['title']

def send_email(sender, senderPassword, receiver, message):
    server = None
    try:
        #create email message
        msg = EmailMessage()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = "Chapter Update!"
        msg.set_content(message)

        context = ssl.create_default_context()

        # this will connect the SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)

        # Login to the server
        server.login(sender, senderPassword)

        # send the email
        server.sendmail(sender, receiver, msg.as_string())

        print("Email sent successfully")
    except Exception as e:
        print('Failed to send email: ', str(e))

    finally:
        if server:
            server.quit()

def isLatestChapter(chapter_number):
    latest_chapter = config.get('latest_chapter', 'latest_chapter', fallback=None)

    if latest_chapter == chapter_number:
        return False
    elif latest_chapter is None or latest_chapter < chapter_number:
        config.set('latest_chapter', 'latest_chapter', chapter_number)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        return True
    else:
        return False

def checkForChapterUpdate():

    global pageNumber
    url = f"{baseUrl}{novelUrl}"

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read()

    soup = BeautifulSoup(html, 'html.parser')

    # pagination is a specific html element within the page that contains the page numbers
    pagination = soup.find('ul', class_='pagination')
    if pagination:
        finalPageUrl = pagination.find('li', class_='PagedList-skipToLast') # this is the button you see that takes you to the final page of the chapter list.
        if finalPageUrl:
            url = f"{baseUrl}{finalPageUrl.find('a')['href']}" # build out the final page url based on the base url and the given href
            req = urllib.request.Request(url, headers=headers) # we need a new scrape of the last chapter page.
            with urllib.request.urlopen(req) as response:
                html = response.read()
            
            soup = BeautifulSoup(html, 'html.parser')
            
            chapterList = soup.find('ul', class_='chapter-list') # find the list of chapters.
            chapters = chapterList.find_all('li')[-8:] # get the last eight chapters (maxiumum i have seen update at once so far from my favoured novel)

            for chapter in chapters:
                chapter_number = chapter['data-chapterno'] # get the chapter number
                chapter_title = chapter.find('a')['title'] # ger get the title of the chapter
                if isLatestChapter(chapter_number): # find out if its the latest chapter
                    message = f"\nThere is a new chapter of {novelTitle}!\n{chapter_title}"
                    send_email(sender, senderPassword, emailNumber, message)
                    time.sleep(60) # wait 1 minute before sending the next sms. If sent too quickly, sometimes it may block the msg or cause delays in sending.
                else:
                    print("No new chapter.")
        else:
            print("No final page found")
    else:
        print("No pagination found")


# check for chapter update every 10 minutes
while True:
    checkForChapterUpdate()
    time.sleep(600)  


