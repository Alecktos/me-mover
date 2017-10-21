from memover import file_handler


class _BiggestFile:
    def __init__(self):
        self.size = 0
        self.path = None


def rename(source_directory):
    # biggest_file = [0, None]
    subtitle_files = []
    biggest_file = _BiggestFile()

    for file in file_handler.get_directory_content(source_directory):
        file_size = file.get_file_size(file)
        if file_size > biggest_file.size:
            biggest_file.size = file_size
            biggest_file.path = file

        if file.endswith(('.srt', '.smi', '.ssa', '.ass', '.vtt')):
            subtitle_files.append(file)




