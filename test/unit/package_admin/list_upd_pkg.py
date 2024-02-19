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

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = {"-i": "Database_Name:Table_Name"}

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)


class Dnf(object):

    """Class:  Dnf

    Description:  Class which is a representation of the Dnf class.

    Methods:
        __init__
        fetch_update_pkgs

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the Dnf class.

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
        test_k_kernel_success
        test_k_kernel_failure
        test_dict_no_k
        test_template_no_k

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.dnf = Dnf()
        self.args = ArgParser()
        self.data = {"Server": "ServerName"}

        self.status = (True, None)
        self.status2 = (False, "Error Message")
        self.results = (True, None)
        self.results2 = (False, "Error Message")

    @mock.patch("package_admin.output_run")
    @mock.patch("package_admin.kernel_check")
    @mock.patch("package_admin.create_template_dict")
    def test_k_kernel_success(self, mock_dict, mock_kernel, mock_run):

        """Function:  test_k_kernel_success

        Description:  Test with -k option, but with kernel check success.

        Arguments:

        """

        self.args.args_array = {"-i": "Database_Name:Table_Name", "-k": True}

        mock_dict.return_value = self.data
        mock_kernel.return_value = (self.status, self.data)
        mock_run.return_value = self.status

        self.assertEqual(
            package_admin.list_upd_pkg(self.args, self.dnf), self.results)

    @mock.patch("package_admin.kernel_check")
    @mock.patch("package_admin.create_template_dict")
    def test_k_kernel_failure(self, mock_dict, mock_kernel):

        """Function:  test_k_kernel_failure

        Description:  Test with -k option, but with kernel check failure.

        Arguments:

        """

        self.args.args_array = {"-i": "Database_Name:Table_Name", "-k": True}

        mock_dict.return_value = self.data
        mock_kernel.return_value = (self.status2, self.data)

        self.assertEqual(
            package_admin.list_upd_pkg(self.args, self.dnf), self.results2)

    @mock.patch("package_admin.output_run")
    def test_dict_no_k(self, mock_run):

        """Function:  test_dict_no_k

        Description:  Test with passed dictionary and no -k option.

        Arguments:

        """

        mock_run.return_value = self.status

        self.assertEqual(
            package_admin.list_upd_pkg(
                self.args, self.dnf, data=self.data), self.results)

    @mock.patch("package_admin.output_run")
    @mock.patch("package_admin.create_template_dict")
    def test_template_no_k(self, mock_dict, mock_run):

        """Function:  test_template_no_k

        Description:  Test with template dictionary and no -k option.

        Arguments:

        """

        mock_dict.return_value = self.data
        mock_run.return_value = self.status

        self.assertEqual(
            package_admin.list_upd_pkg(self.args, self.dnf), self.results)


if __name__ == "__main__":
    unittest.main()
