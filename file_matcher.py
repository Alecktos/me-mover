# coding=utf-8
import os


class FileMatcher:

    def search_file(self, search, path):
        keywords = search.split()  # Split on whitespace
        for file_name in os.listdir(path):
            file_path = path + file_name
            if os.path.isfile(file_path):
                match = self.__match_file(keywords, file_name)
                if match:
                    return file_path
        raise Exception('can not find any matching file.')

    def __match_file(self, keywords, file_name):
        match = True
        for keyword in keywords:
            if not self.__is_keyboard_part_of_filename(keyword, file_name):
                match = False
                break
        return match

    def __is_keyboard_part_of_filename(self, keyword, file_name):
        return keyword.lower() in file_name.lower()  # keyword is part of name
