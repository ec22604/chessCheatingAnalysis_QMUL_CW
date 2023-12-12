## chessCheatingAnalysis

# overview
In order to use the analysis.py, please concatenate the zip parts and unzip the file to find games.csv. 
If on linux, you can use the following command: cat games.zip.part1 games.zip.part2 games.zip.part3 games.zip.part4 > games.zip
If on Windows/Mac, then please use 7zip

# collection.py
collection.py is the python script which is used in order to collect the data from chess.com's API.
Using all of the users in users.csv, it will take approximately 30-45 minutes to collect all of the data if storing on onedrive and about 10-15 minutes if storing locally.
The function in collection.py is tested as part of the unit testing.

