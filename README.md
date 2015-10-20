# episode-mover

Python application for moving TV-show episodes in a specific folder into a three structure.

file names needs to be specified with S01E05 to be moved correctly. The files will be moved to [specified root directory]/[Show name]/Season */


Usage example
-------------

#. Install episode-mover
    python install setup.py

#. Move episodes with episode-mover
    episode-mover -show-name "halt and catch fire" -source "media/inbox-tv-shows" -destination "media/sorted-tv-shows"

        -force              when running script with force command show name folder and season folder will be created if they do not exist.
        -show-name          Name fo the show to search for.
        -source             Directory in witch to look for episode files to be moved.
        -destination        The root directory that find episodes should be moved into.