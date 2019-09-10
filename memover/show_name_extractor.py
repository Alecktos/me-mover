import datetime
import re


def extract_delete_test_dirs_show_name(show_name):
    show_name_words = __extract_urls(show_name) \
        .replace('.', ' ') \
        .split()

    show_name_words = __extract_release_date(show_name_words)
    show_name_words = __extract_sample_word(show_name_words)
    show_name_words = __extract_meta_info(show_name_words)
    show_name_words = __trim_garbage_chars(show_name_words)
    show_name_words = __strip_from_season(show_name_words)
    return ' '.join(show_name_words)


def __extract_urls(show_name):
    if 'www.' not in show_name.lower():
        return show_name

    url_start_index = show_name.find('www.')
    url_end_index = show_name.find(' ', url_start_index)
    show_name = show_name.replace(show_name[url_start_index:url_end_index], '')
    return __extract_urls(show_name)


def __extract_release_date(show_name_words):
    d1 = datetime.date(2000, 1, 1)
    d2 = datetime.date.today()

    try:
        last_word_date = datetime.datetime.strptime(show_name_words[-1], '%Y').date()
        if d1 <= last_word_date <= d2:
            del show_name_words[-1]
    finally:
        return show_name_words


def __extract_sample_word(show_name_words):
    return [re.sub('\W*sample\W*', '', word, 0, re.IGNORECASE) for word in show_name_words]


def __extract_meta_info(show_name_words):
    if '[' in show_name_words and ']' in show_name_words:
        start_meta_info = show_name_words.index('[')
        end_meta_info = show_name_words.index(']')
        del show_name_words[start_meta_info:end_meta_info + 1]
        return __extract_meta_info(show_name_words)

    return show_name_words


def __trim_garbage_chars(show_name_words):
    garbage_chars = ['-']

    if show_name_words[0] in garbage_chars:
        show_name_words.remove(show_name_words[0])
        return __trim_garbage_chars(show_name_words)

    if show_name_words[-1] in garbage_chars:
        show_name_words.remove(show_name_words[-1])
        return __extract_meta_info(show_name_words)

    return show_name_words


def __strip_from_season(show_name_words):
    lower_cases = list(map(str.lower, show_name_words))
    if 'season' in lower_cases:
        strip_from = lower_cases.index('season')
        del show_name_words[strip_from:]
    return show_name_words
