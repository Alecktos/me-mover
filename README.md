# episode-mover

Python application for moving TV-show episodes in a specific folder into a three structure.

file names needs to be specified with S01E05 to be moved correctly. The files will be moved to [specified root directory]/[show name]/[season folder]

## 1. Install episode-mover
        python setup.py install

## 2. Move episodes with episode-mover
### Example:
    episode-mover -show-name "Halt And Catch Fire" -source "media/inbox-tv-shows" -destination "media/sorted-tv-shows" -force
If there for example are a file named Halt.and.Catch.Fire.S02E08.mp4 in media/inbox-tv-shows it will be moved to media/sorted-tv-shows/Halt And Catch Fire/Season 2/Halt.and.Catch.Fire.S02E08.mp4. If that directory does not exist it will be created.

### Commands:
    -force              Show name directory and season directory will be created if they do not exist.
    -show-name          Name of the show to search for.
    -source             Directory in witch to look for episode-files to move.
    -destination        Root directory that found episodes should be moved into.