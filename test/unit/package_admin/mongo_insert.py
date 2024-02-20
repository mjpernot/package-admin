#!/usr/bin/python
# Classification (U)

"""Program:  mongo_insert.py

    Description:  Unit testing of mongo_insert in package_admin.py.

    Usage:
        test/unit/package_admin/mongo_insert.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import package_admin
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_insert_mongo_failure
        test_insert_mongo_successful
        test_no_insert3
        test_no_insert2
        test_no_insert

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.db_tbl = "Database:Table"
        self.class_cfg = "Class Cfg"
        self.data = dict()

        self.status = (True, None)
        self.status2 = (False, "Error Message Here")

        self.results = (True, None)
        self.results2 = (False, "Error Message Here")

    @mock.patch("package_admin.mongo_libs.ins_doc")
    def test_insert_mongo_failure(self, mock_mongo):

        """Function:  test_insert_mongo_failure

        Description:  Test with failed install into MongoDB.

        Arguments:

        """

        mock_mongo.return_value = self.status2

        self.assertEqual(
            package_admin.mongo_insert(
                self.db_tbl, self.class_cfg, self.data), self.results2)

    @mock.patch("package_admin.mongo_libs.ins_doc")
    def test_insert_mongo_successful(self, mock_mongo):

        """Function:  test_insert_mongo_successful

        Description:  Test with successful install into MongoDB.

        Arguments:

        """

        mock_mongo.return_value = self.status

        self.assertEqual(
            package_admin.mongo_insert(
                self.db_tbl, self.class_cfg, self.data), self.results)

    def test_no_insert3(self):

        """Function:  test_no_insert3

        Description:  Test with both arguments set to False.

        Arguments:

        """

        self.assertEqual(
            package_admin.mongo_insert(False, False, self.data), self.results)

    def test_no_insert2(self):

        """Function:  test_no_insert2

        Description:  Test with one argument set to False.

        Arguments:

        """

        self.assertEqual(
            package_admin.mongo_insert(
                False, self.class_cfg, self.data), self.results)

    def test_no_insert(self):

        """Function:  test_no_insert

        Description:  Test with one argument set to False.

        Arguments:

        """

        self.assertEqual(
            package_admin.mongo_insert(
                self.db_tbl, False, self.data), self.results)


if __name__ == "__main__":
    unittest.main()
