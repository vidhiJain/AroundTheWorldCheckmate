# Checkmate

Code for checkmate 2015. Made using Python 3.4 and Django 1.8.

In this checkmate, there will be 2 (or more) servers. There will be one server running Django and housing the database. The other server(s) will have all frontend stuff (HTML pages, images, css, js, etc.). Those will be simple fileservers.
The users will load HTML pages from one of the fileservers. JS code will make ajax calls to the Django backend server.

* All  files are in the folder named `static`.
* All backend non-database data (like config) is stored in the folder named `data`.
* API endpoints are documented in endpoints.html.

### Setup:

1. If you are on a linux system, write `make prepare` in terminal opened in the project's root. This will set up everything for you. If you are on Windows, you'll have to look at `Makefile` and manually run all steps listed in it.
2. Run `python3 manage.py createsuperuser` if you want an administrator.

### During game:

1. Run `python3 scripts/reg_portal.py open` to open registration.
2. Run `python3 scripts/reg_portal.py close` to close registration.
3. Run `python3 scripts/end_game.py` to end the game. This will also close the registration portal.
4. During the game or after it, run `python3 scripts/get_cheaters.py` to get a list of all users who have created multiple accounts using the same IP address.
