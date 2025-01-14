#!/usr/bin/python
# Classification (U)

"""Program:  list_upd_pkg.py

    Description:  Integration testing of list_upd_pkg in package_admin.py.

    Usage:
        test/integration/package_admin/list_upd_pkg.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import mock

try:
    import simplejson as json
except ImportError:
    import json

# Local
sys.path.append(os.getcwd())
import package_admin                        # pylint:disable=E0401,C0413
import lib.gen_class as gen_class           # pylint:disable=E0401,C0413,R0402
import version                              # pylint:disable=E0401,C0413

__version__ = version.__version__


class Yum():

    """Class:  Yum

    Description:  Class which is a representation of the Yum class.

    Methods:
        __init__
        get_hostname
        get_distro
        fetch_update_pkgs

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the Mail class.

        Arguments:

        """

        self.hostname = "Server_Host_Name"
        self.data = {"Package": "PACKAGE_NAME", "Ver": "0.0.0",
                     "Arch": "LINUX", "Repo": "REPO_NAME"}
        self.distro = ("OS_Name", "Version_Release", "Type_Release")

    def get_distro(self):

        """Method:  get_distro

        Description:  Return self.distro attribute.

        Arguments:

        """

        return self.distro

    def get_hostname(self):

        """Method:  get_hostname

        Description:  Return Server's hostname.

        Arguments:

        """

        return self.hostname

    def fetch_update_pkgs(self):

        """Method:  fetch_update_pkgs

        Description:  Return Server's update package data.

        Arguments:

        """

        return self.data


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_list_upd_pkg_file
        test_list_upd_pkg_file_json
        test_list_upd_pkg_sup_std
        test_list_upd_pkg_out_std
        tearDown

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.yum = Yum()
        self.base_dir = "test/integration/package_admin"
        self.test_path = os.path.join(os.getcwd(), self.base_dir)
        self.tmp_path = os.path.join(self.test_path, "tmp")
        self.out_file = os.path.join(self.tmp_path, "package_upd_list.txt")
        self.dbn = "test_sysmon"
        self.tbl = "test_server_pkgs"
        self.array2 = ["./package_admin.py", "-o", self.out_file, "-z"]
        self.args_array2 = gen_class.ArgParser(self.array2)
        self.args_array2.arg_parse2()
        self.args_array2.args_array["-o"] = self.out_file
        self.args_array2.args_array["-z"] = True
        self.array4 = ["./package_admin.py", "-z"]
        self.args_array4 = gen_class.ArgParser(self.array4)
        self.args_array4.arg_parse2()
        self.args_array4.args_array["-z"] = True
        self.array5 = ["./package_admin.py"]
        self.args_array5 = gen_class.ArgParser(self.array5)
        self.time_str = "2018-01-01 01:00:00"

    @mock.patch("package_admin.datetime")
    def test_list_upd_pkg_file(self, mock_date):

        """Function:  test_list_upd_pkg_file

        Description:  Test writing to file.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        package_admin.list_upd_pkg(self.args_array2, self.yum)

        with open(self.out_file, "r", encoding="UTF-8") as fhdr:
            data = json.load(fhdr)

        self.assertIn("Server", data)

    @mock.patch("package_admin.datetime")
    def test_list_upd_pkg_file_json(self, mock_date):

        """Function:  test_list_upd_pkg_file_json

        Description:  Test writing to file in JSON format.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        self.args_array2.args_array["-f"] = True

        package_admin.list_upd_pkg(self.args_array2, self.yum)

        with open(self.out_file, "r", encoding="UTF-8") as fhdr:
            data = json.load(fhdr)

        self.assertIn("Server", data)

    @mock.patch("package_admin.datetime")
    def test_list_upd_pkg_sup_std(self, mock_date):

        """Function:  test_list_upd_pkg_sup_std

        Description:  Test suppressing standard out.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        self.assertEqual(
            package_admin.list_upd_pkg(self.args_array4, self.yum),
            (True, None))

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    @mock.patch("package_admin.datetime")
    def test_list_upd_pkg_out_std(self, mock_date):

        """Function:  test_list_upd_pkg_out_std

        Description:  Test writing to standard out.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        self.assertEqual(
            package_admin.list_upd_pkg(self.args_array5, self.yum),
            (True, None))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:

        """

        if os.path.isfile(self.out_file):
            os.remove(self.out_file)


if __name__ == "__main__":
    unittest.main()
