App screenshots, Icons, Model pictures, and Tutorial screenshots contain various image support files. They probably won't require any modification. 

College_Prep_JSON.txt is the file that Python conversion script outputs to. 

College_Prep.ics is the input for the Python conversion script.
    1. To create it, go to the school portal, and copy the url to RSS feed for the calendar. (Note: this should be the calendar that has the block schedule for the entire school, not a block schedule for an individual. At the top of each day, it should have an event like M2 or T1, and events like B (M2) and Open (R2) throughout the day.)
    2. On a Mac, open Calendar, choose File, New Calendar Subscription... from the top bar, paste in the url, and hit subscribe. This should create a new calendar.
    3. In the list of calendars on the left, select the calendar, then choose File, Export, Export... from the top bar. Choose the destination and file name, making sure the file extension is .ics, and then hit export. The export process isn't instantaneous, but should finish within a minute or two. 

CollegePrepScheduleParser contains the Python conversion script. 
    Main1819.py is the file to be run. It handles reading from the .ics file, does some model correction, and writes the output to the output file. 
    Support1819.py is a support file that actually parses the internals of the .ics file and turns it into a JSON dictionary. 

    Before running the Python conversion script, ensure the following: 
        1. A file named Main1819.py (or Main1920.py, or Main2021.py...) is in the folder.
        2. A file named Support1819.py (or Support1920.py, or Support2021.py...) is in the same folder. 
        3. In Main1819.py ensure that:
            `readPath` is the path to the .ics file. (Note that including "~" in file paths won't work)
            `writePath` is the intended destination. 
            `classesMustBeAfterYear`, `classesMustBeAfterMonth`, and `classesMustBeAfterDay` are properly set to exclude classes from the previous academic year. For example, for the 2018-2019 academic year, the variables were set to 2018, 8, and 1. 

    To run the Python conversion script:
        1. Open Terminal.app (/Applications/Utilities/Terminal.app)
        2. Change the current directory to the CPS Schedule Assets directory. (ex. "cd ~/Desktop/CPS\ Schedule\ Assets" without quotes)
        3. Type "cd CollegePrepScheduleParser" without the quotes and hit enter
        4. Type "python Main1819.py" without the quotes and hit enter
    To upload the file to iCloud:
        1. Open the output file (College_Prep_JSON.txt), choose Edit, Select All, then Edit, Copy. 
        2. In a web browser, go to "https://icloud.developer.apple.com/dashboard", and log in with the school's developer Apple ID and password. 
        3. On the left, under "The College Preparatory School", choose "icloud.cps-appdev.College-Prep-Schedule". 
        4. In the middle, under "Development" or under "Production", choose "Data" (Note: the below process is the same, but any devices that run the app from Xcode will access the data in "Development", while any devices that run the app downloaded from the App Store will use the data in "Production", so it's a good idea to go through this process for both of them.)
        5. On the left, under "Database", change the setting from "Private Database" to "Public Database"
        6. On the left, click "Query Records" In the middle, an item called "Schedule-real" should appear. 
        7. Click on the name "Schedule-real"
        8. On the right, under "Custom Fields", their should be a text box labelled "Data"
        9. Select all the text in the text box, delete it, and the paste in the text from the output file. 
        10. On the right, near the bottom, hit "Save"

Schedule modifications.txt is a file I use to keep track of any modifications I make to the schedule by hand. For example, last year when the schedule shifted to deal with all the smoke, I wrote down all the changes I made to the schedule. These modifications will need to be copy-pasted from Schedule modifications.txt into College_Prep_JSON.txt each time the Python conversion script is run. After making this modifications, it's a good idea to validate the JSON file to catch any typos you might have made. (If there are typos, the Swift app won't crash, but it won't know what the schedule is.) You can validate the JSON on any number of websites like https://jsonlint.com by copy-pasting the contents of the output file into the website and then hit "Validate JSON". 