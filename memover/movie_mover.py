import file_handler
import logger


def move(movie_destination_path, movie_file):
    if file_handler.check_directory_existance(movie_destination_path):
        destination_dir = movie_destination_path + '/' + movie_file.get_movie_name() + '/'
        file_handler.create_dir(destination_dir)
        destination_path = destination_dir + movie_file.get_file_name()
        file_handler.move_file(
            movie_file.get_file_path(), destination_path
        )
    else:
        logger.log('Folder does not exist: ' + movie_destination_path)
