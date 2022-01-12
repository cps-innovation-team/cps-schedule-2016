import os
from cpsparser import *
import json
import requests

__author__ = 'msa'

#####NOTE TO SELF: file paths in main() may need to be updated, if the read and write locations have changed, due to reorganization of files#####

class DAY:
    #used to represent a group of classes
    #contains the classes in self.vevents and the weektype in self.weekType
    def __init__(self, vevent):
        self.vevnts = [vevent]
        self.weekType = vevent.weekType

    def append(self, vevent):
        #adds the vevent to the collection in self
        self.vevnts.append(vevent)

    def description(self):
        #returns the description for all of the vevents in self
        return str([vevent.description() for vevent in self.vevnts])

    def jsonObject(self):
        #returns the json formatted version of self
        return (self.weekType, [vevent.jsonObject() for vevent in self.vevnts])


def main():
    #MARK: path
    readPath = "/Users/msa/Desktop/Xcode Assets/CPS Schedule/College_Prep.ics"
    #any valid path will do, just make sure it ends with a .ics file
    if not os.path.exists(readPath):
        print "Path %s is invalid!" % (readPath)
        os._exit(0)

    #open a file
    with open(readPath) as f:

        #make a list of VEVENT's (classes)
        vevents = [VEVENT(s) for s in veventTextBlocks(str(f.read()))]

        #fill a dictionary of DAY's, formatted {string : DAY}, where the string represents the datetime of the DAY
        days = {}
        for vevent in vevents:
            #MARK: Model awareness
            #there may be issues present in the data, so correct the model here
            if (vevent.summary == "A"
                and vevent.dateStart.isoWeekday() == 1
                and vevent.weekType == "M1"
                and vevent.dateStart.timeFieldsAreEqual(DATETIME.initWithTime(8, 5, 0))
                and vevent.dateEnd.timeFieldsAreEqual(DATETIME.initWithTime(8, 55, 0))):
                    vevent.dateEnd.setTimeTo(DATETIME.initWithTime(8, 50, 0))
            elif (vevent.summary == "Lunch"
                and vevent.dateStart.isoWeekday() == 4
                and vevent.weekType == "R1"
                and vevent.dateStart.timeFieldsAreEqual(DATETIME.initWithTime(11, 40, 0))
                and vevent.dateEnd.timeFieldsAreEqual(DATETIME.initWithTime(12, 25, 0))):
                    vevent.dateStart.setTimeTo(DATETIME.initWithTime(12, 0, 0))
                    vevent.dateEnd.setTimeTo(DATETIME.initWithTime(12, 45, 0))

            #if it exists, append to the DAY in days
            if vevent.dateStart.date() in days:
                days[vevent.dateStart.date()].append(vevent)
            #else, create
            else:
                #MARK: Model awareness
                #if it is before august 2016, do not include it
                if vevent.dateStart.isBefore(DATETIME.initWithDate(2016, 8, 1)):
                    continue

                days[vevent.dateStart.date()] = DAY(vevent)

        #webURL needs to be a valid https string to a valid and current RSS/iCal feed from the website.
        #for future use, after I have graduated, this can be replaced with another student or faculty(?) member
        #it is used to look at special events, like intraterm, cps day, and finals
        webURL = "https://college-prep.myschoolapp.com/podium/feed/iCal.aspx?q=FF3FD419E6A2CC000CE04C827957AE8BF4084310B4325800772D743DC5D29704A0C0028672BB7688BBD224BFAD7B76FF6702BB3B770519DD"
        #2017-18 url is probably https://college-prep.myschoolapp.com/podium/feed/iCal.aspx?z=1nKwIGaMKVLqbz9Usdd7QwrCXmc%2fSFklabVC7EY%2fVyp%2bJbBGTFaa10FGzlvudOAEx02jH5WaFwraAIVKFx14Fw%3d%3d
        print "Will request from internet"
        r = requests.get(webURL)
        print "Did request from internet"
        if r.status_code != 200:
            print "Got status code %s, terminating abruptly" % r.status_code
            os._exit(0)
        else:
            print "Got status code 200, everything is fine"
        #loop through the vevents
        for vevent in [VEVENT(s) for s in veventTextBlocks(r.text)]:
            #this can be replaced with whatever is the special event
            #MARK: Model awareness
            if vevent.summary == "Intraterm ()" or vevent.summary == "CPS Day ()" or vevent.summary == "Finals ()":
                #remove the space and parens
                vevent.summary = vevent.summary[:-3]
                #set to be all day
                vevent.dateStart.setTimeTo(DATETIME.initWithTime(8, 5, 0))
                vevent.dateEnd.setTimeTo(DATETIME.initWithTime(15, 15, 0))
                #set to be a string, being the weekday and then "1", representing ex. monday of week one as M1
                vevent.weekType = ["S", "M", "T", "W", "R", "F"][vevent.dateStart.isoWeekday()] + "1"
                #add to days
                days[vevent.dateStart.date()] = DAY(vevent)

            #this sets the weekType for each DAY by looking at the all day events like M1 and R2
            #for each one, we set the weekType for that DAY
            elif re.match("\w\w \(\)", vevent.summary):
                #MARK: Model awareness
                if vevent.dateStart.date() == "27012017":
                    continue #included in the personal, but not in the bell schedule, a mistake
                days[vevent.dateStart.date()].weekType = vevent.summary[:-3]

        #catch for any errors where the weekType was "0", because this will cause the program to crash
        for date, dayObject in days.iteritems():
            if dayObject.weekType == "0":
                print "Had week type 0, date: %s" % date.description()
                print "terminating abruptly"
                os._exit(0)

        #write
        #MARK: path
        f = "/Users/msa/Desktop/Xcode Assets/CPS Schedule/College_Prep_JSON.txt"
        #this can be any file, just make sure it ends with .txt
        with open(f, "w") as f2:
            f2.write(json.dumps({key : value.jsonObject() for key, value in days.iteritems()}))
            print("Did write to %s" % f)


main()