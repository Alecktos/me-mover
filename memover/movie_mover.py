from . import file_handler, logger


def move(movie_root_path, path):
    if movie_root_path[-1] != '/':
        movie_root_path += '/'

    if file_handler.path_is_directory(path):
        movie_dir = movie_root_path + file_handler.get_last_path_part(path)
        file_handler.create_dir(movie_dir)

        __move_dir(path, movie_dir)
    else:

        movie_dir = movie_root_path + file_handler.get_last_name_from_path(path)
        file_handler.create_dir(movie_dir)

        __move_file(
            path,
            movie_dir + '/' + file_handler.get_last_path_part(path)
        )


def __move_dir(root_source_path, root_destination_path):
    if file_handler.directory_is_empty(root_source_path):
        return

    for relative_source_path in file_handler.get_directory_content(root_source_path):
        source_path = root_source_path + '/' + relative_source_path
        destination_path = root_destination_path + '/' + relative_source_path
        if file_handler.path_is_directory(source_path):
            file_handler.create_dir(destination_path)
            __move_dir(source_path, destination_path)
        else:
            __move_file(
                source_path,
                destination_path
            )


def __move_file(source_path, destination_path):
    file_handler.move(
        source_path,
        destination_path
    )
    logger.info('"' + source_path + '" moved to: "' + destination_path + '"')
