#!/usr/bin/env python3
import requests
import urllib.request
import datetime
import configparser
import time

def reserveRoom(fname, lname, email, phone, length, staff, date, room, lang):
    # set URL that we will direct our request to
    URL = "https://tntech.evanced.info/admin/dibs/api/reservations/post"

    # set headers
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                        ' Chrome/36.0.1941.0 Safari/537.36'), ('Content-Type', 'application/json; charset=utf-8')]
    urllib.request.install_opener(opener)

    # set up key value pairs for the post request variables
    DATA = (
            ('firstName', fname),
            ('lastName', lname),
            ('emailAddress', email),
            ('phoneNumber', phone),
            ('reservationLength', length),
            ('staffAccess', staff),
            ('startDate', date),
            ('roomid', room),
            ('langCode', lang),
            )

    # send data to API as POST request, then print results to console
    r = requests.post(url = URL, data = DATA)
    text = r.json()
    print("\n",text)

def main():
    # take current date, add 4 days to it, and convert it to a suitable string format for DIBS API
    date = ((datetime.date.today() + datetime.timedelta(days=4)).strftime("%Y/%m/%d 16:00:00"))
    print("Trying to reserve Volpe Library room for 2 hours on: " + date)

    # set up parser to config through our .ini file with data of several users
    # the data is required to reserve a room in Volpe Library
    config = configparser.ConfigParser()
    # you must specify full file path for crontab, the path used below is not adequate usually
    config.read("tokens/users.ini")

    # parse through each section in the config file, take the data and submit an API request with reserveRoom()
    for section in config.sections():
        fname = config.get(section, 'firstName')
        lname = config.get(section, 'lastName')
        email = config.get(section, 'email')
        phone = config.get(section, 'phone')
        staff = config.get(section, 'staffAccess')
        length = config.get(section, 'reservationLength')
        room = config.get(section, 'room')
        lang = config.get(section, 'lang')
        reserveRoom(fname, lname, email, phone, length, staff, date, room, lang)
        time.sleep(10)

# auto execute main on script startup
if __name__ == "__main__":
    main()