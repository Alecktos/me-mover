import file_handler


def move(movie_destination_path, movie_file, source_root_path):
    if not file_handler.directory_exist(movie_destination_path):
        raise NoMovieDestinationDir('Folder does not exist: ' + movie_destination_path)

    destination_dir = movie_destination_path + '/' + movie_file.get_movie_name(source_root_path) + '/'

    if not file_handler.directory_exist(destination_dir):
        file_handler.create_dir(destination_dir)

    destination_path = destination_dir + movie_file.get_file_name()
    file_handler.move_file(
        movie_file.get_file_path(), destination_path
    )


class NoMovieDestinationDir(Exception):
    def __init__(self, message):
        super(NoMovieDestinationDir, self).__init__(message)
