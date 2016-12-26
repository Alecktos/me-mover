# episode-mover

Python application for moving TV-show episodes in a specific folder into a tree structure.

file names needs to be specified with S01E05 to be moved correctly. The files will be moved to [specified root directory]/[show name]/[season folder]

## 1. Install episode-mover
        python setup.py install

## 2. Move episodes with episode-mover
### Example:
    episode-mover -show-name "Halt And Catch Fire" -source "media/inbox-tv-shows" -destination "media/sorted-tv-shows"
If there for instance are two files named Halt.and.Catch.Fire.S02E08.mp4 and Halt.and.Catch.Fire.S02E09.mp4 in media/inbox-tv-shows these will be moved to media/sorted-tv-shows/Halt And Catch Fire/Season 2/Halt.and.Catch.Fire.S02E08.mp4 (Halt.and.Catch.Fire.S02E09.mp4 will be placed in the same directory). If the show or season directory does not exist it will be created.

### Commands:
    -show-name          Name of the show to search for.
    -source             Directory in witch to look for episode-files to move.
    -destination        Root directory that found episodes should be moved into.
