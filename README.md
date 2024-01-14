# chessCheatingAnalysis

## overview
In order to use the analysis.py, please concatenate the zip parts and unzip the file to find games.csv (the games.csv in the repo is empty). \
If on linux, you can use the following command: cat games.zip.part1 games.zip.part2 games.zip.part3 games.zip.part4 games.zip.part5> games.zip\
If on Windows/Mac, then please use 7zip or an online tool (https://pinetools.com/join-files)\
Alternatively, you can run collection.py and use the resulting games.csv file (although please note that this will get the most up-to-date information and could cause small discrepancies between the report graphs and the graphs displayed from analysis.py)

This repository uses the python unittest module to unit testing\
This repository also uses circleCI in order to achieve Continuous Intergration

## collection.py
collection.py is the python script which is used in order to collect the data from chess.com's API.\
Using all of the users in users.csv, it will take approximately 30-45 minutes to collect all of the data if storing on onedrive and about 10-15 minutes if storing locally.\
The function in collection.py is tested as part of the unit testing.

## analysis.py
analysis.py is the python script which has all of the analysis graphs used in the report. It also has all of its functions tested as part of the unittesting\
In order to use plt.show() and see the graphs, you must have all of the modules installed from requirements.txt. Please run the command 'pip install -r requirements.txt' in order to do this.\
Specifically, If you are recieving an error similar to the following:\ 
UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown\
then you need to make sure that you have PyQt5 installed (found in the requirements.txt) or some other module which matplotlib can use for visualisation (for example, tkinter)

It may take up to 10 minutes to initialise the dataframe before graphs can be displayed - this is due to the large size of the games.csv file
## test.py
test.py is the python script which has all of the unittests for the code, and is what circleCI uses to test. It has 23 tests testing 12 functions.\
For a textual description of the tests, please see tests.md
