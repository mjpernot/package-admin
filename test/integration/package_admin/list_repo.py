#!/usr/bin/python
# Classification (U)

"""Program:  list_repo.py

    Description:  Integration testing of list_repo in package_admin.py.

    Usage:
        test/integration/package_admin/list_repo.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import filecmp
import mock

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
        self.data = ['REPOSITORY_LIST']
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

    def fetch_repos(self):

        """Method:  fetch_repos

        Description:  Return Server's update package data.

        Arguments:

        """

        return self.data


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_list_repo_file
        test_list_repo_file_json
        test_list_repo_sup_std
        test_list_repo_out_std
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
        self.out_path = os.path.join(self.test_path, "out")
        self.tmp_path = os.path.join(self.test_path, "tmp")
        self.out_file = os.path.join(self.tmp_path, "package_repo.txt")
        self.non_json_file = os.path.join(self.out_path,
                                          "package_repo_non_json")
        self.json_file = os.path.join(self.out_path, "package_repo_json")
        self.dbn = "test_sysmon"
        self.tbl = "test_server_pkgs"
        self.array2 = ["-o", self.out_file, "-z", True]
        self.args_array2 = gen_class.ArgParser(self.array2)
        self.array4 = ["-z", True]
        self.args_array4 = gen_class.ArgParser(self.array4)
        self.array5 = ["-z", False]
        self.time_str = "2018-01-01 01:00:00"

    @unittest.skip("file_cmp is failing in Python 3 - Investigate")
    @mock.patch("package_admin.datetime")
    def test_list_repo_file(self, mock_date):

        """Function:  test_list_repo_file

        Description:  Test writing to file.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        package_admin.list_repo(self.args_array2, self.yum)

        status = filecmp.cmp(self.out_file, self.non_json_file)

        self.assertTrue(status)

    @unittest.skip("file_cmp is failing in Python 3 - Investigate")
    @mock.patch("package_admin.datetime")
    def test_list_repo_file_json(self, mock_date):

        """Function:  test_list_repo_file_json

        Description:  Test writing to file in JSON format.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        self.args_array2.args_array["-f"] = True

        package_admin.list_repo(self.args_array2, self.yum)

        status = filecmp.cmp(self.out_file, self.json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.datetime")
    def test_list_repo_sup_std(self, mock_date):

        """Function:  test_list_repo_sup_std

        Description:  Test suppressing standard out.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        self.assertEqual(
            package_admin.list_repo(self.args_array4, self.yum),
            (True, None))

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    @mock.patch("package_admin.datetime")
    def test_list_repo_out_std(self, mock_date):

        """Function:  test_list_repo_out_std

        Description:  Test writing to standard out.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        self.assertEqual(
            package_admin.list_repo(self.args_array2, self.yum),
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
