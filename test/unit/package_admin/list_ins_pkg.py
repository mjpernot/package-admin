#!/usr/bin/python
# Classification (U)

"""Program:  list_ins_pkg.py

    Description:  Unit testing of list_ins_pkg in package_admin.py.

    Usage:
        test/unit/package_admin/list_ins_pkg.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party
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
        test_mongo_failure
        test_mongo_successful
        test_list_upd_pkg

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class Yum(object):

            """Class:  Yum

            Description:  Class which is a representation of the Yum class.

            Methods:
                __init__
                fetch_install_pkgs

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the Mail class.

                Arguments:

                """

                self.hostname = ""
                self.data = ""

            def fetch_install_pkgs(self):

                """Method:  fetch_install_pkgs

                Description:  Set self.data attribute.

                Arguments:

                """

                self.data = "Installed_Packages_List"

        self.yum = Yum()

        self.args_array = {"-i": "Database_Name:Table_Name"}
        self.func_name = self.yum.fetch_install_pkgs
        self.status = (True, None)
        self.status2 = (False, "Error Message")
        self.results = (False, "list_ins_pkg: Error Message")

    @mock.patch("package_admin.process_yum")
    def test_mongo_failure(self, mock_yum):

        """Function:  test_mongo_failure

        Description:  Test with failed Mongo connection.

        Arguments:

        """

        mock_yum.return_value = self.status2

        self.assertEqual(package_admin.list_ins_pkg(self.args_array, self.yum),
                         self.results)

    @mock.patch("package_admin.process_yum")
    def test_mongo_successful(self, mock_yum):

        """Function:  test_mongo_successful

        Description:  Test with successful Mongo connection.

        Arguments:

        """

        mock_yum.return_value = self.status

        self.assertEqual(package_admin.list_ins_pkg(self.args_array, self.yum),
                         self.status)

    @mock.patch("package_admin.process_yum")
    def test_list_ins_pkg(self, mock_yum):

        """Function:  test_list_ins_pkg

        Description:  Test call to list_ins_pkg function.

        Arguments:

        """

        mock_yum.return_value = self.status

        self.assertEqual(package_admin.list_ins_pkg(self.args_array, self.yum),
                         self.status)


if __name__ == "__main__":
    unittest.main()
