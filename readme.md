# Link to Webapp [https://github-network-app.herokuapp.com/]

# Github Network App

This is still a work in progress.


The app redirects the user to the github login page and then retrieves the oauthentication token once the user has successfully logged in. The app will then redirect the user back to there github profile. Later, I will use the token to retrieve all of the users repos, collaborators, followers, etc and display it back in a network graph.

## Prerequisites

To install the flask app, you need:
- python3
- python packages in the requirements.txt file
 
 Install the packages with
``` 
 pip install -r requirements.txt
```

## Installing

On a MacOS/linux system, installation is easy. Open a terminal, and go into 
the directory with the flask app files. Run `python worldbank.py` in the terminal.
