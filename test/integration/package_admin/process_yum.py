#!/usr/bin/python
# Classification (U)

"""Program:  process_yum.py

    Description:  Integration testing of process_yum in package_admin.py.

    Usage:
        test/integration/package_admin/process_yum.py

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

        Description:  Set self.hostname attribute.

        Arguments:

        """

        return self.hostname

    def fetch_update_pkgs(self):

        """Method:  fetch_update_pkgs

        Description:  Set self.data attribute.

        Arguments:

        """

        return self.data


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_process_yum_file
        test_process_yum_file_json
        test_process_yum_sup_std
        test_process_yum_out_std
        tearDown

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.yum = Yum()
        self.dict_key = "Update_Packages"
        self.func_name1 = self.yum.fetch_update_pkgs
        self.base_dir = "test/integration/package_admin"
        self.test_path = os.path.join(os.getcwd(), self.base_dir)
        self.out_path = os.path.join(self.test_path, "out")
        self.tmp_path = os.path.join(self.test_path, "tmp")
        self.out_file = os.path.join(self.tmp_path, "package_list.txt")
        self.non_json_file = os.path.join(
            self.out_path, "package_proc_list_non_json")
        self.json_file = os.path.join(self.out_path, "package_proc_list_json")
        self.dbn = "test_sysmon"
        self.tbl = "test_server_pkgs"
        self.array2 = ["-o", self.out_file, "-z", True, "-f", True]
        self.args_array2 = gen_class.ArgParser(self.array2)
        self.array3 = ["-i", "test_sysmon:test_server_pkgs", "-z", True]
        self.args_array3 = gen_class.ArgParser(self.array3)
        self.array4 = ["-z", True]
        self.args_array4 = gen_class.ArgParser(self.array4)
        self.array5 = ["-z", False]
        self.args_array5 = gen_class.ArgParser(self.array5)
        self.array6 = ["-o", self.out_file, "-z", True]
        self.args_array6 = gen_class.ArgParser(self.array6)
        self.time_str = "2018-01-01 01:00:00"
        self.results = (True, None)

    @unittest.skip("file_cmp is failing in Python 3 - Investigate")
    @mock.patch("package_admin.datetime")
    def test_process_yum_file(self, mock_date):

        """Function:  test_process_yum_file

        Description:  Test writing to file.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        package_admin.process_yum(
            self.args_array2, self.yum, self.dict_key, self.func_name1)

        status = filecmp.cmp(self.out_file, self.non_json_file)

        self.assertTrue(status)

    @unittest.skip("file_cmp is failing in Python 3 - Investigate")
    @mock.patch("package_admin.datetime")
    def test_process_yum_file_json(self, mock_date):

        """Function:  test_process_yum_file_json

        Description:  Test writing to file in JSON format.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        package_admin.process_yum(
            self.args_array6, self.yum, self.dict_key, self.func_name1)

        status = filecmp.cmp(self.out_file, self.json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    @mock.patch("package_admin.datetime")
    def test_process_yum_sup_std(self, mock_date):

        """Function:  test_process_yum_sup_std

        Description:  Test suppressing standard out.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        self.assertEqual(
            package_admin.process_yum(
                self.args_array4, self.yum, self.dict_key, self.func_name1),
            self.results)

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    @mock.patch("package_admin.datetime")
    def test_process_yum_out_std(self, mock_date):

        """Function:  test_process_yum_out_std

        Description:  Test writing to standard out.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        self.assertEqual(
            package_admin.process_yum(
                self.args_array5, self.yum, self.dict_key, self.func_name1),
            self.results)

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:

        """

        if os.path.isfile(self.out_file):
            os.remove(self.out_file)


if __name__ == "__main__":
    unittest.main()
