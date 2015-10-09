# coding=utf-8
import os
import logger

#TODO: os things should be refactored out

class FileMatcher:

    def search_files(self, search, path):
        files = []
        keywords = search.split()  # Split on whitespace
        for file_name in os.listdir(path):
            file_path = path + file_name
            if not os.path.isfile(file_path):
                continue

            match = self.__match_file(keywords, file_name)
            if match:
                logger.log('Found file: ' + file_path)
                files.append(file_path)
        return files

    def __match_file(self, keywords, file_name):
        match = True
        for keyword in keywords:
            if not self.__is_keyboard_part_of_filename(keyword, file_name):
                match = False
                break
        return match

    def __is_keyboard_part_of_filename(self, keyword, file_name):
        return keyword.lower() in file_name.lower()  # keyword is part of name
