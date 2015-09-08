# Checkmate

Code for checkmate 2015. Made using Python 3.4 and Django 1.8.

In this checkmate, there will be 2 (or more) servers. There will be one server running Django and housing the database. The other server(s) will have all frontend stuff (HTML pages, images, css, js, etc.). Those will be simple fileservers.
The users will load HTML pages from one of the fileservers. JS code will make ajax calls to the Django backend server.

* All  files are in the folder named `static`.
* All backend non-database data (like config) is stored in the folder named `data`.
* API endpoints are documented in endpoints.html.

### Setup:

1. If you are on a linux system, write `make prepare` in terminal opened in the project's root. This will set up everything for you. If you are on Windows, you'll have to look at `Makefile` and manually run all steps listed in it under the heading 'prepare'.
2. Run `python3 manage.py createsuperuser` if you want an administrator.

### During game:

1. Use `scripts/status.py` to control registration and access to the game. Its command line arguments are documented below.
1. Run `python3 scripts/end_game.py` to end the game. This will also close registration and disallow access to game.
2. During the game or after it, run `python3 scripts/get_cheaters.py` to get a list of all users who have created multiple accounts using the same IP address.

### status.py:

There are 2 portals: registration portal and game portal

* When the registration portal is open, people can register and get a team account
* When the game portal is open, people can play checkmate
* People can always see the leaderboard

Running the script:

1. `python3 scripts/status.py` : shows the status of all portals
2. `python3 scripts/status.py (open|close)` : open or close all portals
3. `python3 scripts/status.py [portal_name]` : shows the status of the specified portal
4. `python3 scripts/status.py [portal_name] (open|close)` : open or close the specified portal
