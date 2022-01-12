import re
import datetime

__author__ = 'msa'

def veventTextBlocks(s):
    """convert a long string `s` into an array of strings that are formatted for VEVENT.__init__()"""

    #use re.split to include the delimiter
    #this gives some meta data at the start, then PATTERN, moreData, PATTERN, moreData
    splitReads = re.split(r"(BEGIN:VEVENT)", s)
    #join to be PATTERNmoreData, PATTERNmoreData
    joinedSplits = [splitReads[i] + splitReads[i + 1] for i in xrange(len(splitReads)) if splitReads[i] == "BEGIN:VEVENT"]

    return joinedSplits

class VEVENT:
    def __init__(self, s):
        #s is a block of text, identified by main() to be a valid VEVENT
        #break by lines, ignoring empty lines
        fields = filter(lambda x: x != "", s.split("\r\n"))
        #dict comprehension, so that I can query for fields by the ICS name
        #relavant properties will be accessed using dot notation
        #take a line and split on :
        #the first half is the key, the second half is the value
        self.dict = {line.split(":")[0] : line.split(":")[1] for line in fields}

        #the value at SUMMARY might be formatted "foo (M1)", signifying monday, week one
        #use re.sub to replace occurences of ~space paren letter_for_day number_for_week paren~ with ""
        #and stick that in self.summary
        self.summary = self.dict["SUMMARY"]

        #make a DATETIME with the text at the DTSTART and DTEND keys
        #but the key has a couple different formats
        #so just take the first one that starts with DTSTART or DTEND
        startKey = [key for key, value in self.dict.iteritems() if key.startswith("DTSTART")][0]
        endKey = [key for key, value in self.dict.iteritems() if key.startswith("DTEND")][0]

        self.dateStart = DATETIME(self.dict[startKey])
        self.dateEnd = DATETIME(self.dict[endKey])

        #MARK: Model awareness
        #split into form "foo (letter", "number", ")", then take 2 from the end as an int
        #however, if before august 2016, we set to 0 (as a string), to try to catch it if it slips through
        #if we fail, we also want it to be 0
        self.weekType = "0"
        if self.dateStart.isAfter(DATETIME.initWithDate(2016, 8, 1)):
            try:
                self.weekType = re.split("(\(|\))", self.dict["SUMMARY"])[-3]
            except IndexError:
                pass
                #self.weekType is still "0"

    def description(self):
        return "Summary: %s\nStart: %s\nEnd: %s" % (self.summary, self.dateStart.description(), self.dateEnd.description())

    def jsonObject(self):
        return {"name" : self.summary, "start" : self.dateStart.time(), "end" : self.dateEnd.time() }

class DATETIME:
    #starts with an empty string for ease of 1-indexing
    MONTHS = ["", "January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

    def __init__(self, s):
        #init time parts in case we return early
        #maybe this should be a string? later on, we string subscript, but maybe it doesn't matter
        #because this is only relevant for when we are passed a string that only contains date information
        self.hour = 0
        self.minute = 0
        self.second = 0

        #s is formatted `YYYYMMDDThhmmss`
        #with the `T` being a literal delimiter in s
        self.year = s[:4]
        self.month = s[4:6]
        self.day = s[6:8]

        #if passed a short string, we were only passed the date, and we pre-initalized the time parts, so we can return early
        if len(s) == 8: return
        #otherwise, fill in the real time parts
        #delimiter `T` at index 8, so hour starts at index 9
        self.hour = s[9:11]
        self.minute = s[11:13]
        self.second = s[13:15]

    @classmethod
    def initWithNumbers_YMD_HMS(cls, year, month, day, hour, minute, second):
        #for ease of use for creating DATETIMES
        year = str(year).zfill(4)
        month = str(month).zfill(2)
        day = str(day).zfill(2)
        hour = str(hour).zfill(2)
        minute = str(minute).zfill(2)
        second = str(second).zfill(2)

        return DATETIME("%s%s%sT%s%s%s" % (year, month, day, hour, minute, second))

    @classmethod
    def initWithDate(cls, year, month, day):
        #for ease of use for creating DATETIMEs
        return DATETIME.initWithNumbers_YMD_HMS(year, month, day, 0, 0, 0)

    @classmethod
    def initWithTime(cls, hour, minute, second):
        #for ease of use for creating DATETIMES
        return DATETIME.initWithNumbers_YMD_HMS(0, 0, 0, hour, minute, second)

    def time(self):
        #time representation as an HHMMSS string
        return "%s%s%s" % (self.hour, self.minute, self.second)

    def date(self):
        #date representation as a DDMMYYYY string
        return "%s%s%s" % (self.day, self.month, self.year)

    def description(self):
        #a human-readable description of self
        return "%s %s, %s at %s:%s:%s" % (self.day, DATETIME.MONTHS[int(self.month)], self.year, self.hour, self.minute, self.second)

    def isAfter(self, other):
        #returns a bool indicating if self is after other
        if int(self.year) > int(other.year): return True
        if int(self.year) == int(other.year):
            if int(self.month) > int(other.month): return True
            if int(self.month) == int(other.month):
                if int(self.day) > int(other.day): return True
                if int(self.day) == int(other.day): return False
                if int(self.day) < int(other.day): return False
            if int(self.month) < int(other.month): return False
        if int(self.year) < int(other.year): return False

    def isBefore(self, other):
        #returns a bool indicating if self is before other
        return (not self.allFieldsAreEqual(other)) and (not self.isAfter(other))

    def allFieldsAreEqual(self, other):
        #returns a bool indicating if the time fields and the date fields are equal in self and other
        #often used like `if aDatetime.allFieldsAreEqual(DATETIME.initWithNumbers_YMD_HMS(2016, 9, 1, 8, 5, 0)):`
        return self.timeFieldsAreEqual(other) and self.dateFieldsAreEqual(other)

    def timeFieldsAreEqual(self, other):
        #returns a bool indicating if the time fields are equal in self and other
        #often used like `if aDatetime.timeFieldsAreEqual(DATETIME.initWithTime(8, 5, 0):`
        return (self.hour == other.hour
                and self.minute == other.minute
                and self.second == other.second)

    def dateFieldsAreEqual(self, other):
        #returns a bool indicating if the date fields are equal in self and other
        #often used like `if aDatetime.dateFieldsAreEqual(DATETIME.initWithDate(2016, 9, 1)):`
        return (self.year == other.year
                and self.month == other.month
                and self.day == other.day)

    def setTimeTo(self, other):
        #copies the time fields from other into self
        self.hour = other.hour
        self.minute = other.minute
        self.second = other.second

    def setDateTo(self, other):
        #copies the date fields from other into self
        self.year = other.year
        self.month = other.month
        self.day = other.day

    def copyFrom(self, other):
        #copies the date and time fields from other into self
        self.setDateTo(other)
        self.setTimeTo(other)

    def isoWeekday(self):
        #returns the iso weekday number of self
        #monday = 1, ... sunday = 7
        return datetime.date(int(self.year), int(self.month), int(self.day)).isoweekday()