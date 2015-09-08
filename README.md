# Checkmate

Code for checkmate 2015. Made using Python 3.4 and Django 1.8.

* All WebGL files are in the folder named `static`.
* All backend non-database data (like config) is stored in the folder named `data`.

### Setup:

1. If you are on a linux system, write `make prepare` in terminal opened in the project's root. This will set up everything for you. If you are on Windows, you'll have to look at `Makefile` and manually run all steps listed in it.
2. Run `python3 manage.py createsuperuser` if you want an administrator.

### During game:

1. Run `python3 scripts/reg_portal.py open` to open registration.
2. Run `python3 scripts/reg_portal.py close` to close registration.
3. Run `python3 scripts/end_game.py` to end the game. this will also close the registration portal.
4. During the game or after it, run `python3 scripts/get_cheaters.py` to get a list of all users who have created multiple accounts using the same IP address.
