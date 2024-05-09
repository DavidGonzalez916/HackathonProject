# HackathonProject
This is my Hackathon Project, It is a webscraper that grabs statistics from a table on espn. 
I installed selenium, pypyodbc, and pandas. 
I used SQL Server to host a database that connects to python and stores the statistics that were webscraped. 
I have a stored procedure saved on my SQL Database by the name of updatePlayers that updates the players and statistics when the program is run.
It is possible to add 6 additional statistics FG%, 3P%, FT%, STL, BLK, TO by typing those specific flags into the command line after question.
the table resets and removes those additional statistics on each passby.
