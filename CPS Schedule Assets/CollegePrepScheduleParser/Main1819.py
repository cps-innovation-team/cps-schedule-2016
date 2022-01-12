import os
from Support1819 import *
import json
import requests

__author__ = 'msa'

#####NOTE TO SELF: file paths in main() may need to be updated, if the read and write locations have changed, due to reorganization of files#####

#MARK
readPath = "/Users/msa/Desktop/College_Prep.ics"
writePath = "/Users/msa/Desktop/College_Prep_JSON.txt"


classesMustBeAfterYear = 2018
classesMustBeAfterMonth = 8
classesMustBeAfterDay = 1


class DAY:
    #used to represent a group of classes
    #contains the classes in self.vevents and the weektype in self.weekType
    def __init__(self, vevent):
        self.vevents = [vevent]
        self.weekType = vevent.weekType

    def append(self, vevent):
        #adds the vevent to the collection in self
        self.vevents.append(vevent)

    def description(self):
        #returns the description for all of the vevents in self
        return str([vevent.description() for vevent in self.vevents])

    def jsonObject(self):
        #returns the json formatted version of self
        return (self.weekType, [vevent.jsonObject() for vevent in self.vevents])


def main():
    #any valid path will do, just make sure it ends with a .ics file
    if not os.path.exists(readPath):
        print "File input path %s does not exist" % (readPath)
        print "Open Main1819.py, change `readPath` to a valid .ics file, and rerun"
        print "If you forgot to change the readPath, you may have also forgotten to change the write path"
        print "You might also have forgotten to set the `classesMustBeAfter` variables to exclude classes that happened in the previous academic year"
        os._exit(0)
    print "Had valid file input path"
    print "Will include all classes after %s-%s-%s" % (classesMustBeAfterYear, classesMustBeAfterMonth, classesMustBeAfterDay)

    #open a file
    with open(readPath) as f:

        #make a list of VEVENT's (classes)
        vevents = [VEVENT(s) for s in veventTextBlocks(str(f.read()))]

        #fill a dictionary of DAY's, formatted {string : DAY}, where the string represents the datetime of the DAY
        days = {}
        for vevent in vevents:
            #MARK: Model awareness
            #there may be issues present in the data, so correct the model here

            if vevent.summary == "Advising Check-In (T2)":
                vevent.summary = "Advising Check In (T2)"
            if vevent.summary == " C (F2)":
                vevent.summary = "C (F2)"
            #NEW#
            if vevent.summary[-4:] == "(RS)":
                vevent.summary = vevent.summary[:-4] + "(R1)"
            if vevent.summary == "AMC Testing":
                continue
            if vevent.summary == "Advising Check-In":
                vevent.summary = "Advising Check In (T2)"
            #END NEW#

            #if it exists, append to the DAY in days
            if vevent.dateStart.date() in days:
                days[vevent.dateStart.date()].append(vevent)
            #else, create
            else:
                #MARK: Model awareness
                #if it is before august of this year, do not include it
                y = classesMustBeAfterYear
                m = classesMustBeAfterMonth
                d = classesMustBeAfterDay
                if vevent.dateStart.isBefore(DATETIME.initWithDate(y, m, d)):
                    continue

                days[vevent.dateStart.date()] = DAY(vevent)


#re.sub(r" \((M|T|W|R|F)(1|2)\)", "", foo)

        
        for strDate in days:
            day = days[strDate]
            day.weekType = day.vevents[0].summary[-3:-1]
            for vevent in day.vevents:
                vevent.summary = vevent.summary[:-5]

        #catch for any errors where the weekType was "0", because this will cause the Swift app to crash
        for date, dayObject in days.iteritems():
            if dayObject.weekType == "0":
                print "Had week type 0, date: %s" % date.description()
                print "terminating abruptly"
                os._exit(0)

        #write
        #this can be any file, just make sure it ends with .txt
        with open(writePath, "w") as f2:
            f2.write(json.dumps({key : value.jsonObject() for key, value in days.iteritems()}))
            print("Did write to %s" % writePath)


main()