import file_handler
import logger


class FileMatcher:

    def search_files(self, search, path):
        files = []
        keywords = search.split()  # Split on whitespace
        for file_name in file_handler.get_subdirectories(path):
            file_path = path + '/' + file_name

            match = self.__match_file(keywords, file_name)
            if match:
                logger.log('Found file/folder: ' + file_path)
                files.append(file_path)

        if not files:
            logger.log('No matching files found')
        return files

    def __match_file(self, keywords, file_name):
        for keyword in keywords:
            if not self.__is_keyword_part_of_filename(keyword, file_name):
                return False
        return True

    def __is_keyword_part_of_filename(self, keyword, file_name):
        return keyword.lower() in file_name.lower()  # keyword is part of name
