# episode-mover

Python application for moving TV-show episodes in a specific folder into a three structure.

file names needs to be specified with S01E05 to be moved correctly. The files will be moved to [specified root directory]/[show name]/[season folder]

## 1. Install episode-mover
        python install setup.py

## 2. Move episodes with episode-mover
### * Example:
    episode-mover -show-name "Halt And Catch Fire" -source "media/inbox-tv-shows" -destination "media/sorted-tv-shows" -force
If there are for example a file named Halt.and.Catch.Fire.S02E08.mp4 in media/inbox-tv-shows it will be moved to media/sorted-tv-shows/Halt And Catch Fire/Season 2/Halt.and.Catch.Fire.S02E08.mp4. If that directory do not exist et will be created.

### * Commands:
    -force              when running script with force command show name directory and season directory will be created if they do not exist.
    -show-name          Name fo the show to search for.
    -source             Directory in witch to look for episode files to be moved.
    -destination        The root directory that find episodes should be moved into.