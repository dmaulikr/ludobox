#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A python script will generate the following files : a list of all games and a
folder containing info of each game.
"""
# TODO make the code testable by providing a way to pass the input and output
#   folders has parameter to a function

# TODO make the code python3 compatible: print function and some few other

import os

# json is used to read game descriptions as they are stored as JSON files for
# easy "low tech" compliant sharing.
import json

# Jinja2 is used as a template engine to generate the list of games as an HTML5
# compliant table.
# To get it: sudo pip install Jinja2
from jinja2 import Environment, FileSystemLoader

# slugify is used to generate clean HTML/URL compliant strings from any unicode
# string while keeping readability. We use it here to generate clean file name
# for all generated files.
# To get it: sudo pip install python-slugify
from slugify import slugify

ACCEPTED_TYPES=["jpg","png","gif", "stl", "pdf"]

# Input directory where we should find JSON files each describing one game
DATA_DIR = os.path.join(os.getcwd(), "data")

# Output dirrectory where we generate the pages:
#   *   one directory for each game filled with all the revelent data: HTML
#       description of the game, attached files, docmentation...
#   *   the wellcome page that gives access to everything
#   *   the add page that allow us to add a new game
GAMES_DIR = os.path.join(os.getcwd(), "games") # output

# TODO test this function with different scenari: inexistant dir, info.json
#   present/absent, with/without attached file
def read_game_info(path):
    """
    Read all the info available about the game stored at the provided path.

    Arguments:
    path -- directory where the game info and data are stored

    Returns (ok, data) where ok is a boolean indicating if the data retrieval
    when well and data is a dictionary containing the game data. If ok is false
    data is empty. You should always test it first:

    >>> ok, data = read_game_info("stupid_path")
    >>> if not ok:
    ...     print "something went wrong"
    something went wrong

    The game data can come from:
    *   the info.json file
    *   the attached files found in the dir
    *   somme are also computed from other data like a cleaned name suitable for
        url generation (slugified name)
    """
    # Load JSON from the description file of the game
    json_path = os.path.join(path, "info.json")
    try:
        with open(json_path, "r") as json_file:
            data = json.load( json_file )
    except IOError, e:
        return False, {}

    # Add permalink
    data["slug"] = slugify(data["title"])

    return True, data


# TODO split this function in many diffrent small func
def main():
    # TODO move this piece of code closer to where it is needed
    # First we need templates from files
    env = Environment(loader=FileSystemLoader('templates'))
    single_template = env.get_template('single.html') # display a single game
    index_template = env.get_template('index.html') # list all games
    add_template = env.get_template('add.html') # create new game

    # Then we create the games directory
    if not os.path.exists(GAMES_DIR):
        os.makedirs(GAMES_DIR)

    # This stores all JSON from the different games
    games = []

    # We list all folders in "games"
    for path in os.listdir(DATA_DIR):
        if os.path.isdir(os.path.join(DATA_DIR, path)): # check all dir

            # Parse game dir
            data_path = os.path.join(DATA_DIR, path)
            print "Read game info:", data_path,
            ok, game_data = read_game_info(data_path)
            if not ok:
                print "FAIL"
                continue
            print "SUCCESS"
            games.append(game_data)

            # Create game dir
            game_path =  os.path.join(GAMES_DIR, game_data["slug"])
            if not os.path.exists(game_path):
                os.makedirs(game_path)

            # Render template
            single = single_template.render(game_data)
            single_index_path = os.path.join(game_path, "index.html")

            # Write game index.html
            with open(single_index_path , "wb") as single_index:
                single_index.write(single.encode('utf-8'))

    # We now write the root index.html
    index = index_template.render({"games" : games}) # pass games as a dict to jinja2
    main_index_path = os.path.join(GAMES_DIR, "index.html")

    with open(main_index_path , "wb") as main_index :
        main_index.write(index.encode('utf-8'))

    # We then write the add page
    add = add_template.render() # pass games as a dict to jinja2
    add_path = os.path.join(GAMES_DIR, "add")

    # create add path
    if not os.path.exists(add_path):
        os.makedirs(add_path)

    # create add game form
    with open(os.path.join(add_path, "index.html") , "wb") as add_file :
        add_file.write(add.encode('utf-8'))


# TODO add a generate action to specificaly launch a generation
# TODO add a clean action to specificaly launch a cleanup of all generated files
# TODO add a default action/help action that describe the usage and actions
if __name__ == "__main__":
    main()