from memover import file_handler


def rename(source_directory):

    for path in file_handler.get_directory_content(source_directory):
        if file_handler.path_is_directory(path):
            pass


