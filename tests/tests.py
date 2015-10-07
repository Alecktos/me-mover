import os
import unittest
import sys
from file_matcher_test import FileMatcherTest
from file_mover_test import FileMoverTest


def run_test_suit():
    runner = unittest.TextTestRunner()
    test_suite = get_suite()
    runner.run(test_suite)


def get_suite():
    suite = unittest.TestSuite()
    suite.addTest(FileMoverTest())
    suite.addTest(FileMatcherTest())
    return suite

if __name__ == '__main__':
    run_test_suit()
