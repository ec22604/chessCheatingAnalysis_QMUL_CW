# chessCheatingAnalysis

## overview
In order to use the analysis.py, please concatenate the zip parts and unzip the file to find games.csv. \
If on linux, you can use the following command: cat games.zip.part1 games.zip.part2 games.zip.part3 games.zip.part4 > games.zip\
If on Windows/Mac, then please use 7zip or an online tool\
Alternatively, you can run collection.py and use the resulting games.csv file\

This repository uses the python unittest module to unit testing\
This repository also uses circleCI in order to achieve Continuous Intergration

## collection.py
collection.py is the python script which is used in order to collect the data from chess.com's API.\
Using all of the users in users.csv, it will take approximately 30-45 minutes to collect all of the data if storing on onedrive and about 10-15 minutes if storing locally.\
The function in collection.py is tested as part of the unit testing.

## analysis.py
analysis.py is the python script which has all of the analysis graphs used in the report. It also has all of its functions tested as part of the unittesting\
In order to use plt.show() and see the graphs, you must have all of the modules installed from requirements.txt. Please run the command 'pip install -r requirements.txt' in order to do this.

## test.py
test.py is the python script which has all of the unittests for the code, and is what circleCI uses to test. It has 23 tests testing 12 functions
