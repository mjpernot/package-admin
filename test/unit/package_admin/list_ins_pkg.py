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
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import package_admin                            # pylint:disable=E0401,C0413
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class ArgParser():                                      # pylint:disable=R0903

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


class Yum():                                            # pylint:disable=R0903

    """Class:  Yum

    Description:  Class which is a representation of the Yum class.

    Methods:
        __init__
        fetch_install_pkgs

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the Yum class.

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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_list_ins_pkg_fail
        test_list_upd_pkg

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.yum = Yum()
        self.args = ArgParser()
        self.func_names = self.yum.fetch_install_pkgs
        self.status = (True, None)
        self.status2 = (False, "Error Message")
        self.results = (False, "list_ins_pkg: Error Message")

    @mock.patch("package_admin.process_yum")
    def test_list_ins_pkg_fail(self, mock_yum):

        """Function:  test_list_ins_pkg_fail

        Description:  Test call with failed return.

        Arguments:

        """

        mock_yum.return_value = self.status2

        self.assertEqual(
            package_admin.list_ins_pkg(self.args, self.yum), self.results)

    @mock.patch("package_admin.process_yum")
    def test_list_ins_pkg(self, mock_yum):

        """Function:  test_list_ins_pkg

        Description:  Test call with successful return.

        Arguments:

        """

        mock_yum.return_value = self.status

        self.assertEqual(
            package_admin.list_ins_pkg(self.args, self.yum), self.status)


if __name__ == "__main__":
    unittest.main()
