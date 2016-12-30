# me-mover

Python application for moving movies and tv-shows in a specified file structure.

TV-shows will be moved to ``[sorted tv-show root directory]/[show name]/[season folder]`` Movies will be moved to ``[movie destination directory]``

## 1. Install me-mover
        git clone https://github.com/Alecktos/me-mover.git
        cd me-mover
        
        python setup.py install 
        # or run it directly 
        python -m memover

## 2. Move episodes with episode-mover
### Examples:
    memover tvshow -show-name "halt and catch fire" -show-source sourcefolder -show-destination media/sorted-tv-shows
Halt.and.Catch.Fire.S02E08.mp4 and Halt.and.Catch.Fire.S02E09.mp4 in media/inbox-tv-shows these will be moved to media/sorted-tv-shows/Halt And Catch Fire/Season 2/Halt.and.Catch.Fire.S02E08.mp4 (Halt.and.Catch.Fire.S02E09.mp4 will be placed in the same directory). If the show or season directory does not exist it will be created.

    memover file -file-path sourcefolder/Star.Wars.The.Clone.Wars.BluRay.1080p.x264.5.1.mp4 -show-destination media/sorted-tv-shows -movie-destination media/movies
Will move the movie to the media/movies/Star.Wars.The.Clone.Wars.BluRay.1080p.x264.5.1.mp4

    file -file-path sourcefolder/Vikings.S04E15.720p.mkv -show-destination media/sorted-tv-shows -movie-destination media/movies    
Will move episode 15 Season 4 of Vikings to media/sorted-tv-shows/Vikings/Season 4/Vikings.S04E15.720p.mkv

### Commands:
    tvshow              Moves all found episodes of a specified tv-show
    file                Moves a movie or tv-show episode    

### Arguments:
    -file-path          Movie or tv-show file to move.
    -show-name          Name of the show to search for.
    -show-source        Directory in witch to look for episodes to move.
    -show-destination   Destination root directory for tv-shows.
    -movie-destination  Destination directory for movies
