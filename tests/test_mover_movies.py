import unittest

from memover import file_handler, mover
from tests.utils import file_mover_tester


class TestMoverMovies(unittest.TestCase, file_mover_tester.FileMoverTester):

    def setUp(self):
        self._create_test_dirs()

    def tearDown(self):
        self._delete_test_dirs()

    def test_move_movie_by_file_path(self):
        movie_file_name = 'Abcde Fgh ijk Wjere To Found In 2010 HD-AA x111-ABC.mkv'
        file_handler.create_file(self._SOURCE_DIRECTORY + '/' + movie_file_name)

        source_file_path = self._SOURCE_DIRECTORY + '/' + movie_file_name
        mover.move_media_by_path(source_file_path, self._SHOW_DESTINATION_DIRECTORY, self._MOVIE_DESTINATION_DIRECTORY)

        destination_path = self._MOVIE_DESTINATION_DIRECTORY + '/' + file_handler.get_last_name_from_path(movie_file_name) + '/' + movie_file_name
        self._assert_file_moved(source_file_path, destination_path)

    def test_moving_movie_in_directory(self):
        folder_path = self._SOURCE_DIRECTORY + '007 Going For Old Time HD-TS x264-CPG'
        file_handler.create_dir(folder_path)
        file_path = folder_path + '/007 Going For Old Time HD-TS x264-CPG.mp4'
        file_handler.create_file(file_path)
        mover.move_media_by_path(folder_path, self._SHOW_DESTINATION_DIRECTORY, self._MOVIE_DESTINATION_DIRECTORY)
        file_destination_path = self._MOVIE_DESTINATION_DIRECTORY + '007 Going For Old Time HD-TS x264-CPG/007 Going For Old Time HD-TS x264-CPG.mp4'
        self._assert_file_moved(file_path, file_destination_path)

    def test_moving_movie_with_image(self):
        folder_path = self._SOURCE_DIRECTORY + 'Konstig (2017) [1080p] [JKL.KL]'
        file_handler.create_dir(folder_path)
        source_file_path = folder_path + '/WWW.YTS.AG.jpg'
        file_handler.create_file(source_file_path)

        mover.move_media_by_path(folder_path, self._SHOW_DESTINATION_DIRECTORY, self._MOVIE_DESTINATION_DIRECTORY)

        file_destination_path = self._MOVIE_DESTINATION_DIRECTORY + '/Konstig (2017) [1080p] [JKL.KL]/WWW.YTS.AG.jpg'
        self._assert_file_moved(source_file_path, file_destination_path)

    def test_moving_movies_by_name(self):
        file_1_folder_path = self._SOURCE_DIRECTORY + '/201 Coolings 1999.DVDRIP.Xvid.NVesub-'
        file_handler.create_dir(file_1_folder_path)
        file_1_path = file_1_folder_path + '/201 Coolings 1999.___RIP.Xvid.NVesub-123.mp4'
        file_handler.create_file(file_1_path)

        file_2_path = self._SOURCE_DIRECTORY + '/201 Coolings 200.DADRAP.NVesub.mp4'
        file_handler.create_file(file_2_path)

        mover.move_media_by_name(
            '201 Coolings',
            self._SOURCE_DIRECTORY,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY
        )

        file_destination_path = self._MOVIE_DESTINATION_DIRECTORY + '/201 Coolings 1999.DVDRIP.Xvid.NVesub-/201 Coolings 1999.___RIP.Xvid.NVesub-123.mp4'
        self._assert_file_moved(file_1_folder_path, file_destination_path)

        file_destination_path = self._MOVIE_DESTINATION_DIRECTORY + '/201 Coolings 200.DADRAP.NVesub/201 Coolings 200.DADRAP.NVesub.mp4'
        self._assert_file_moved(file_2_path, file_destination_path)

    def test_moving_movie_with_extra_dir(self):
        movie_dir = 'Movie.The.Movie.1234'
        file_handler.create_dir(self._SOURCE_DIRECTORY + movie_dir)

        movie_file = movie_dir + '/Movie.The.Movie.1234.mkv'
        file_handler.create_file(self._SOURCE_DIRECTORY + movie_file)

        extras_dir = movie_dir + '/Extras'
        file_handler.create_dir(self._SOURCE_DIRECTORY + extras_dir)

        extras_file1 = extras_dir + '/Movie.The.Movie.1234.Theatrical.Trailer.mkv'
        file_handler.create_file(self._SOURCE_DIRECTORY + extras_file1)

        extras_file2 = extras_dir + '/Movie.3.Theatrical.Trailer.mkv'
        file_handler.create_file(self._SOURCE_DIRECTORY + extras_file2)

        extras_soundtrack_dir = extras_dir + '/Soundtrack Live'
        file_handler.create_dir(self._SOURCE_DIRECTORY + extras_soundtrack_dir)

        extras_soundtrack_file1 = extras_soundtrack_dir + '/Making.the.Soundtrack.mkv'
        file_handler.create_file(self._SOURCE_DIRECTORY + extras_soundtrack_file1)

        extras_soundtrack_file2 = extras_soundtrack_dir + '/original.song.mkv'
        file_handler.create_file(self._SOURCE_DIRECTORY + extras_soundtrack_file2)

        mover.move_media_by_path(
            self._SOURCE_DIRECTORY + movie_dir,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY
        )

        self._assert_file_moved(movie_file, self._MOVIE_DESTINATION_DIRECTORY + movie_file)
        self._assert_file_moved(extras_file1, self._MOVIE_DESTINATION_DIRECTORY + extras_file1)
        self._assert_file_moved(extras_file2, self._MOVIE_DESTINATION_DIRECTORY + extras_file2)
        self._assert_file_moved(extras_soundtrack_file1, self._MOVIE_DESTINATION_DIRECTORY + extras_soundtrack_file1)
        self._assert_file_moved(extras_soundtrack_file2, self._MOVIE_DESTINATION_DIRECTORY + extras_soundtrack_file2)

    def test_movie_destination_no_slash_in_path(self):
        dir_name = 'Tah Felling Out Of hope In Valley (2019) [Converted] [movie-test-no-path]/'
        file_handler.create_dir(self._SOURCE_DIRECTORY + dir_name)
        movie_file = 'Tah.Fellingr Out Of hope In Valley.2019.1080p.Converted-[movie-test-no-path].mp4'
        file_handler.create_file(self._SOURCE_DIRECTORY + dir_name + movie_file)

        mover.move_media_by_path(
            self._SOURCE_DIRECTORY + dir_name,
            self._SHOW_DESTINATION_DIRECTORY,
            self._MOVIE_DESTINATION_DIRECTORY[:-1]
        )

        self._assert_file_moved(
            self._SOURCE_DIRECTORY + dir_name + movie_file,
            self._MOVIE_DESTINATION_DIRECTORY + dir_name + movie_file
        )
