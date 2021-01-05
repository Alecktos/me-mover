# me-mover

Me-mover is an application for organizing movies and tv-shows.

TV shows will be moved to ``[tv-show destination directory]/[show name]/[season directory]``. 

Movies will be moved to ``[movie destination directory]/[movie name directory]``

## 1. Install me-mover
### pip
```
> pip install me-mover
```
### From source
```
> git clone https://github.com/Alecktos/me-mover.git
> cd me-mover

> python setup.py install
> python memover
# or run it directly 
> python -m memover
```

## 2. Usage
### By-name
Moves a movie or tv-show from a source directory by searching for its name.
```    
> me-mover by-name {name} {source-dir-path} {show-destination-dir-path} {movie-destination-dir-path}
```
#### Example
```
> me-mover by-name "halt and catch fire" sourcedir media/sorted-tv-shows media/movies

If following files exist:
* `sourcedir/Halt.and.Catch.Fire.S02E08.mp4` 
* `sourcedir/Halt.and.Catch.Fire.S02E09.mp4` 

They will be moved to 
* `media/sorted-tv-shows/Halt And Catch Fire/Season 2/Halt.and.Catch.Fire.S02E08.mp4` 
* `media/sorted-tv-shows/Halt And Catch Fire/Season 2/Halt.and.Catch.Fire.S02E09.mp4`
```
### By-path
Moves a movie or tv-show by its path.
```
> me-mover by-path {source-path} {show-destination-dir-path} {movie-destination-path}
```
#### Example
```
> me-mover by-path sourcefolder/Star.Wars.The.Clone.Wars.BluRay.1080p.x264.5.1.mp4 media/sorted-tv-shows media/movies

Movie will be moved to `media/movies/Star.Wars.The.Clone.Wars.BluRay.1080p.x264.5.1/Star.Wars.The.Clone.Wars.BluRay.1080p.x264.5.1.mp4`

> me-mover by-path sourcefolder/Vikings.S04E15.720p.mkv media/sorted-tv-shows media/movies

Episode will be moved to `media/sorted-tv-shows/Vikings/Season 4/Vikings.S04E15.720p.mkv`
```

### Watch
Watches a directory and moves new files that are placed in it. Assuming that it's either a movie or tv-show.
```
> me-mover watch {source-dir-path} {show-destination-path} {movie-destination-path}
```
#### Example

```
> me-mover watch media/inbox media/sorted-tv-shows media/movies

When moving Vikings.S04E15.720p.mkv to media/inbox
It will be moved to media/sorted-tv-shows/Vikings/Season 4/Vikings.S04E15.720p.m
```

### Commands
    by-name                Moves all found episodes of specified tv-show. If matching movie all movies matching that name will be moved
      positional arguments:
        name                name of TV show or movie to move
        source              source directory to look for media in
        shows-destination   show destination directory
        movies-destination  movie destination directory

    by-path                Moves a movie or tv-show episode.
      positional arguments:
        source              source path of movie or TV show to move
        shows-destination   show destination directory
        movies-destination  movie destination directory

    watch                  Monitors changes in a specific directory.
      positional arguments:
        source                source directory to to watch for incoming TV shows and movies
        shows-destination     show destination directory
        movies-destination    movie destination directory
      optional arguments:
        --quit QUIT, -q QUIT  Number of seconds until exit

### Subtitles
Subtitles of types .srt, .smi, .ssa, .ass, .vtt will be renamed to the name of the video being moved.

### Misc
A parent directory will be created for each moved movie.

If the show name or season directory does not exist they will be created.

## Development


### Run tests
    python -m unittest discover tests

## Requirements
Python 3.8

watchdog
