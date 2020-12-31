from api.models import Event
from bs4 import BeautifulSoup
import urllib.request
import ssl
import json
import os
from datetime import datetime
from django.core.files.storage import default_storage

# Defining format key function
def formatKey(string):
    string = string[:-1]
    string = string.lower()
    string = string.replace(' ', '-')
    return string

# Function to make title of scrapped event to a useable filename
def formatStringFilename(string):
    # Defining all characters that will be removed
    remove_characters = ["/", "!", "?", "(", ")", "#", "$", "%", "^", "&", "*", "+", "=", ",", "{", "}", "[", "]", "-"]
    string = string.lower()
    string = string.replace(" ", "_")
    for character in remove_characters:
        string = string.replace(character, "")
    return string

# Function to strip string until number found
def stripUntilNumber(string):
    for i in range(1, 10):
        index=string.find(str(i))
        if index !=-1 :
            return string[index:] 

# String checking if numbers are in it
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

# Getting browsing page data

def addEvents():
    ssl._create_default_https_context = ssl._create_unverified_context

    # This restores the same behavior as before.
    context = ssl._create_unverified_context()
    print('aaaa\n\n')

    totalUrlList = []
    pageIndex = 1

    # Looping
    while True:
        
        # Trying to get url if cant breaking loop

        try:
            url = "https://rallylist.com/browse-protest-and-rallies/page/" + str(pageIndex)
            source = urllib.request.urlopen(url, context=context).read()
            soup = BeautifulSoup(source, features="html.parser")
        except Exception as e:
            print('page not found breaking loop')
            break

        urlList = []

        # Scrapping links and list of events
        for aTag in soup.find_all('a'):
            try:
                # Checking if title link
                if aTag.get('itemprop') == 'url':
                    # Getting url
                    url = aTag.get('href')
                    if url is not 'https://rallylist.com':
                        if url not in totalUrlList:
                            print(url)
                            totalUrlList.append(url)
                            urlList.append(url)
            except Exception as e:
                print(e)
        if len(urlList) == 0:
            print('page empty breaking loop')
            break
            
        pageIndex += 1
    print(totalUrlList)


    totalEventList = []

    # Looping through events and getting data
    for url in totalUrlList:
        try:
            source = urllib.request.urlopen(url, context=context).read()
            soup = BeautifulSoup(source, features="html.parser")
        except Exception as e:
            print('page not found continuing')
            continue
        eventDict = {}
        
        # Wrapping data scrap in try method
        try:
            # Getting title of event
            header = soup.find_all(attrs={'class' : 'entry-title'})
            print("header.string")
            header = header[0].string
            eventDict['title'] = header

            # Getting image url
            image = soup.find_all(attrs={'class' : 'wp-post-image'})
            image = image[0]
            imageSrc = image.get('src')
            print(imageSrc)
            eventDict['image-url'] = imageSrc

            # Getting image from url and generating title
            resource = urllib.request.urlopen(imageSrc)
            filename = formatStringFilename(eventDict['title']) + ".png"

            # Creating path in media folder and saving file
            path = os.path.join("event_pics", filename)
            default_storage.save(path, resource)

            
            # # Getting description of services
            # pTags = soup.find_all('p')
            # description = None
            # for p in pTags:
            #     # Getting p tag string and wrapping in try method
            #     print(p.string)
            #     if p.string:
            #         description = p.string
                    
            # print("description")
            # print(description)
            # if not description:
            #     eventDict['description'] = description

            # Getting divs
            for div in soup.find_all(attrs={'class' : 'ap-each-custom'}):
                for title in div.find_all(attrs={'class' : 'ap-custom-label'}):
                    
                    # Formating key
                    dataKey = formatKey(title.string)
                    print(dataKey)
                for value in div.find_all(attrs={'class' : 'ap-custom-value'}):
                    dataValue = value.string
                    print(dataValue)

                # Adding value to dict
                eventDict[dataKey] = dataValue

            print(eventDict)
            
            timeStr = eventDict['time-of-event'].strip()
            
            # Checking if colon is in string and changing formating method
            if ':' in timeStr[0 : 4]:
                timeStr = timeStr[0 : 6].strip()
            else:
                timeStr = timeStr[0 : 4].strip()
            
            if hasNumbers(timeStr[0 : 4]) == False:
                timeStr = stripUntilNumber(timeStr)

            datetimeStr = eventDict['date-of-event'] +  " " + timeStr
            
            if datetimeStr[-1] == 'p' or datetimeStr[-1] == 'P' or datetimeStr[-1] == 'a' or datetimeStr[-1] == 'A':
                datetimeStr += 'M'
            # Trying to convert to datetime object
            print(datetimeStr)
            # Changing format method if colon in datetime str
            try:
                datetime_object = datetime.strptime(datetimeStr, '%A, %d %B, %Y %I %p')
                print('datetime success')
            except Exception as e:
                print(e)
                try:
                    datetime_object = datetime.strptime(datetimeStr, '%A, %d %B, %Y %I:%M %p')
                    print('datetime success')
                except Exception as e:
                    print(e)
                    print('datetime failure')
                    continue

            # Checking if item exists
            itemExists = Event.objects.filter(
                title=header,
                image=path,
                organizer=eventDict['organizer'],
                date=datetime_object,
                address=eventDict['address']
            ).exists()

            # If item doesn't exists creating item
            if itemExists == False:
                event = Event.objects.create(
                    title=header,
                    image=path,
                    organizer=eventDict['organizer'],
                    date=datetime_object,
                    address=eventDict['address'],
                    city=eventDict['city']
                )
            print('success')
            # Appending dict to total events
            totalEventList.append(eventDict)
        except Exception as e:
            print(e)
            print('scrap failed continuing')
            continue

    print(totalEventList)
    # with open('event.txt', 'w') as outfile:
    #     json.dump(totalEventList, outfile)

