# me-mover

Python application for moving movies and tv-shows in a specified file structure.

TV-shows will be moved to ``[sorted tv-show root directory]/[show name]/[season folder]``. Movies will be moved to ``[movie destination directory]``

## 1. Install me-mover
        git clone https://github.com/Alecktos/me-mover.git
        cd me-mover
        
        python setup.py install
        python memover
        # or run it directly 
        python -m memover

## 2. Move episodes and movies with me-mover
### Examples:
    me-mover by-name "halt and catch fire" sourcefolder media/sorted-tv-shows media/movies
Halt.and.Catch.Fire.S02E08.mp4 and Halt.and.Catch.Fire.S02E09.mp4 in media/inbox-tv-shows these will be moved to media/sorted-tv-shows/Halt And Catch Fire/Season 2/Halt.and.Catch.Fire.S02E08.mp4 (Halt.and.Catch.Fire.S02E09.mp4 will be placed in the same directory). If the show or season directory does not exist it will be created.

    me-mover by-path sourcefolder/Star.Wars.The.Clone.Wars.BluRay.1080p.x264.5.1.mp4 media/sorted-tv-shows media/movies
Will move the movie to the media/movies/Star.Wars.The.Clone.Wars.BluRay.1080p.x264.5.1.mp4

    me-mover by-path sourcefolder/Vikings.S04E15.720p.mkv media/sorted-tv-shows media/movies    
Will move Vikings season 4 episode 15 of to media/sorted-tv-shows/Vikings/Season 4/Vikings.S04E15.720p.mkv

### Commands:
    by-name                Moves all found episodes of specified tv-show. If matching movie all movies matching that name will be moved
      positional arguments:
        name                name of show or movie to move
        source              source directory to look for media in
        shows-destination   show destination directory
        movies-destination  movie destination directory

    by-path                Moves a movie or tv-show episode.
      positional arguments:
        source              source path of movie or tv-show to moveia in
        shows-destination   show destination directory
        movies-destination  movie destination directory

    watch                  Monitors changes in a specific directory.
      positional arguments:
        source                source directory to to watch for incoming tv-shows or movies
        shows-destination     show destination directory
        movies-destination    movie destination directory
      optional arguments:
        --quit QUIT, -q QUIT  Number of seconds until exit

### Subtitles
Subtitles of types .srt, .smi, .ssa, .ass, .vtt will be renamed to the name of the video being moved.

### Misc
A parent directory will be created for each moved movie.

## Development


### Run tests
    python -m unittest discover tests

## Requirements
Python 3.7
