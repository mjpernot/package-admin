#!/usr/bin/python
# Classification (U)

"""Program:  run_program.py

    Description:  Integration testing of run_program in package_admin.py.

    Usage:
        test/integration/package_admin/run_program.py

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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_run_program_upd_file
        test_run_program_upd_file_json
        test_run_program_upd_sup_std
        test_run_program_upd_out_std
        test_run_program_ins_file
        test_run_program_ins_file_json
        test_run_program_ins_sup_std
        test_run_program_ins_out_std
        test_run_program_repo_file
        test_run_program_repo_file_json
        test_run_program_repo_sup_std
        test_run_program_repo_out_std
        tearDown

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for integration testing.

        Arguments:

        """

        self.base_dir = "test/integration/package_admin"
        self.test_path = os.path.join(os.getcwd(), self.base_dir)
        self.out_path = os.path.join(self.test_path, "out")
        self.tmp_path = os.path.join(self.test_path, "tmp")
        self.out_file = os.path.join(self.tmp_path, "package_out.txt")
        self.list_non_json_file = os.path.join(self.out_path,
                                               "package_list_non_json")
        self.list_json_file = os.path.join(self.out_path, "package_list_json")
        self.upd_non_json_file = os.path.join(self.out_path,
                                              "package_upd_list_non_json")
        self.upd_json_file = os.path.join(self.out_path,
                                          "package_upd_list_json")
        self.ins_non_json_file = os.path.join(self.out_path,
                                              "package_ins_list_non_json")
        self.ins_json_file = os.path.join(self.out_path,
                                          "package_ins_list_json")
        self.repo_non_json_file = os.path.join(self.out_path,
                                               "package_repo_non_json")
        self.repo_json_file = os.path.join(self.out_path,
                                           "package_repo_json")
        self.func_dict1 = {"-L": package_admin.list_ins_pkg,
                           "-U": package_admin.list_upd_pkg,
                           "-R": package_admin.list_repo}
        self.dbn = "test_sysmon"
        self.tbl = "test_server_pkgs"
        self.hostname = "Server_Host_Name"
        self.distro = ("OS_Name", "Version_Release", "Type_Release")
        self.upd_data = {"Package": "PACKAGE_NAME", "Ver": "0.0.0",
                         "Arch": "LINUX", "Repo": "REPO_NAME"}
        self.ins_data = {"Package": "PACKAGE_NAME", "Ver": "0.0.0",
                         "Arch": "LINUX"}
        self.repo_data = ['REPOSITORY_LIST']
        self.array2 = ["-o", self.out_file, "-z", True]
        self.args_array2 = gen_class.ArgParser(self.array2)
        self.array4 = ["-z", True]
        self.args_array4 = gen_class.ArgParser(self.array4)
        self.array5 = ["-z", False]
        self.args_array5 = gen_class.ArgParser(self.array5)
        self.time_str = "2018-01-01 01:00:00"

    @unittest.skip("file_cmp is failing in Python 3 - Investigate")
    @mock.patch("package_admin.gen_dnf.Dnf.get_distro")
    @mock.patch("package_admin.gen_dnf.Dnf.fetch_update_pkgs")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_upd_file(
            self, mock_date, mock_host, mock_data, mock_distro):

        """Function:  test_run_program_upd_file

        Description:  Test writing to file for update option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.args_array2.args_array["-U"] = True

        package_admin.run_program(self.args_array2, self.func_dict1)

        status = filecmp.cmp(self.out_file, self.list_non_json_file)

        self.assertTrue(status)

    @unittest.skip("file_cmp is failing in Python 3 - Investigate")
    @mock.patch("package_admin.gen_dnf.Dnf.get_distro")
    @mock.patch("package_admin.gen_dnf.Dnf.fetch_update_pkgs")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_upd_file_json(
            self, mock_date, mock_host, mock_data, mock_distro):

        """Function:  test_run_program_upd_file_json

        Description:  Test writing to file in JSON format for update option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.args_array2.args_array["-f"] = True
        self.args_array2.args_array["-U"] = True

        package_admin.run_program(self.args_array2, self.func_dict1)

        status = filecmp.cmp(self.out_file, self.list_json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.gen_dnf.Dnf.fetch_update_pkgs")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_upd_sup_std(self, mock_date, mock_host, mock_data):

        """Function:  test_run_program_upd_sup_std

        Description:  Test suppressing standard out for update option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname

        self.args_array4.args_array["-U"] = True
        self.args_array4.args_array["-z"] = True

        self.assertFalse(
            package_admin.run_program(self.args_array4, self.func_dict1))

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_dnf.Dnf.fetch_update_pkgs")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_upd_out_std(self, mock_date, mock_host, mock_data):

        """Function:  test_run_program_upd_out_std

        Description:  Test writing to standard out for update option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname

        self.args_array5.args_array["-U"] = True

        self.assertFalse(
            package_admin.run_program(self.args_array5, self.func_dict1))

    @unittest.skip("file_cmp is failing in Python 3 - Investigate")
    @mock.patch("package_admin.gen_dnf.Dnf.get_distro")
    @mock.patch("package_admin.gen_dnf.Dnf.fetch_install_pkgs")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_ins_file(
            self, mock_date, mock_host, mock_data, mock_distro):

        """Function:  test_run_program_ins_file

        Description:  Test writing to file for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.args_array2.args_array["-L"] = True

        package_admin.run_program(self.args_array2, self.func_dict1)

        status = filecmp.cmp(self.out_file, self.ins_non_json_file)

        self.assertTrue(status)

    @unittest.skip("file_cmp is failing in Python 3 - Investigate")
    @mock.patch("package_admin.gen_dnf.Dnf.get_distro")
    @mock.patch("package_admin.gen_dnf.Dnf.fetch_install_pkgs")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_ins_file_json(
            self, mock_date, mock_host, mock_data, mock_distro):

        """Function:  test_run_program_ins_file_json

        Description:  Test writing to file in JSON format for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.args_array2.args_array["-f"] = True
        self.args_array2.args_array["-L"] = True

        package_admin.run_program(self.args_array2, self.func_dict1)

        status = filecmp.cmp(self.out_file, self.ins_json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.gen_dnf.Dnf.fetch_install_pkgs")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_ins_sup_std(self, mock_date, mock_host, mock_data):

        """Function:  test_run_program_ins_sup_std

        Description:  Test suppressing standard out for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname

        self.args_array4.args_array["-L"] = True
        self.args_array4.args_array["-z"] = True

        self.assertFalse(
            package_admin.run_program(self.args_array4, self.func_dict1))

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_dnf.Dnf.fetch_install_pkgs")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_ins_out_std(self, mock_date, mock_host, mock_data):

        """Function:  test_run_program_ins_out_std

        Description:  Test writing to standard out for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname

        self.args_array5.args_array["-L"] = True

        self.assertFalse(
            package_admin.run_program(self.args_array5, self.func_dict1))

    @unittest.skip("file_cmp is failing in Python 3 - Investigate")
    @mock.patch("package_admin.gen_dnf.Dnf.get_distro")
    @mock.patch("package_admin.gen_dnf.Dnf.fetch_repos")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_repo_file(
            self, mock_date, mock_host, mock_data, mock_distro):

        """Function:  test_run_program_repo_file

        Description:  Test writing to file for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.args_array2.args_array["-R"] = True

        package_admin.run_program(self.args_array2, self.func_dict1)

        status = filecmp.cmp(self.out_file, self.repo_non_json_file)

        self.assertTrue(status)

    @unittest.skip("file_cmp is failing in Python 3 - Investigate")
    @mock.patch("package_admin.gen_dnf.Dnf.get_distro")
    @mock.patch("package_admin.gen_dnf.Dnf.fetch_repos")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_repo_file_json(
            self, mock_date, mock_host, mock_data, mock_distro):

        """Function:  test_run_program_repo_file_json

        Description:  Test writing to file in JSON format for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.args_array2.args_array["-f"] = True
        self.args_array2.args_array["-R"] = True

        package_admin.run_program(self.args_array2, self.func_dict1)

        status = filecmp.cmp(self.out_file, self.repo_json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.gen_dnf.Dnf.fetch_repos")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_repo_sup_std(self, mock_date, mock_host, mock_data):

        """Function:  test_run_program_repo_sup_std

        Description:  Test suppressing standard out for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname

        self.args_array4.args_array["-R"] = True
        self.args_array4.args_array["-z"] = True

        self.assertFalse(
            package_admin.run_program(self.args_array4, self.func_dict1))

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_dnf.Dnf.fetch_repos")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_repo_out_std(self, mock_date, mock_host, mock_data):

        """Function:  test_run_program_repo_out_std

        Description:  Test writing to standard out for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname

        self.args_array5.args_array["-R"] = True

        self.assertFalse(
            package_admin.run_program(self.args_array5, self.func_dict1))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:

        """

        if os.path.isfile(self.out_file):
            os.remove(self.out_file)


if __name__ == "__main__":
    unittest.main()
