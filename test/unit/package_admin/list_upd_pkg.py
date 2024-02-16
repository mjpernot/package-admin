#!/usr/bin/python
# Classification (U)

"""Program:  list_upd_pkg.py

    Description:  Unit testing of list_upd_pkg in package_admin.py.

    Usage:
        test/unit/package_admin/list_upd_pkg.py

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


class ArgParser(object):

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        get_val
        get_args_keys

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = {"-i": "Database_Name:Table_Name"}


class Yum(object):

    """Class:  Yum

    Description:  Class which is a representation of the Yum class.

    Methods:
        __init__
        fetch_update_pkgs

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the Yum class.

        Arguments:

        """

        self.hostname = ""
        self.data = ""

    def fetch_update_pkgs(self):

        """Method:  fetch_update_pkgs

        Description:  Set self.data attribute.

        Arguments:

        """

        self.data = "Update_Package_List"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_list_upd_pkg

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.yum = Yum()
        self.args = ArgParser()
        self.data = {"Server": "ServerName"}

        self.status = (True, None)
        self.status2 = (False, "Error Message")
        self.results = (True, None)

### STOPPED HERE
    @mock.patch("package_admin.process_yum")
    def test_list_upd_pkg(self, mock_yum):

        """Function:  test_list_upd_pkg

        Description:  Test call to test_list_upd_pkg function.

        Arguments:

        """

        mock_yum.return_value = self.status

        self.assertEqual(
            package_admin.list_upd_pkg(self.args, self.yum), self.results)


if __name__ == "__main__":
    unittest.main()
