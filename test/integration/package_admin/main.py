#!/usr/bin/python
# Classification (U)

"""Program:  main.py

    Description:  Unit testing of main in package_admin.py.

    Usage:
        test/integration/package_admin/main.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import filecmp
import mock

try:
    import simplejson as json
except ImportError:
    import json

# Local
sys.path.append(os.getcwd())
import package_admin                        # pylint:disable=E0401,C0413
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import version                              # pylint:disable=E0401,C0413

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_main_upd_file
        test_main_upd_file_json
        test_main_upd_sup_std
        test_main_upd_out_std
        test_main_ins_file
        test_main_ins_file_json
        test_main_ins_sup_std
        test_main_ins_out_std
        test_main_repo_file
        test_main_repo_file_json
        test_main_repo_sup_std
        test_main_repo_out_std
        test_main_arg_dir_chk_crt_false
        test_main_arg_cond_rep_false
        test_main_help_func_true
        tearDown

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for integration testing.

        Arguments:

        """

        self.main = "main.py"
        self.base_dir = "test/integration/package_admin"
        self.test_path = os.path.join(os.getcwd(), self.base_dir)
        self.out_path = os.path.join(self.test_path, "out")
        self.tmp_path = os.path.join(self.test_path, "tmp")
        self.out_file = os.path.join(self.tmp_path, "package_out.txt")
        self.dbn = "test_sysmon"
        self.tbl = "test_server_pkgs"
        self.hostname = "Server_Host_Name"
        self.distro = ("OS_Name", "Version_Release", "Type_Release")
        self.upd_data = {"Package": "PACKAGE_NAME", "Ver": "0.0.0",
                         "Arch": "LINUX", "Repo": "REPO_NAME"}
        self.ins_data = {"Package": "PACKAGE_NAME", "Ver": "0.0.0",
                         "Arch": "LINUX"}
        self.repo_data = ['REPOSITORY_LIST']
        self.argv_list2 = [os.path.join(self.base_dir, self.main),
                           "-o", self.out_file, "-z"]
        self.argv_list4 = [os.path.join(self.base_dir, self.main), "-z"]
        self.argv_list5 = [os.path.join(self.base_dir, self.main)]
        self.time_str = "2018-01-01 01:00:00"

    @mock.patch("package_admin.gen_dnf.Dnf.get_distro")
    @mock.patch("package_admin.gen_dnf.Dnf.fetch_update_pkgs")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_upd_file(self, mock_date, mock_host, mock_data, mock_distro):

        """Function:  test_main_upd_file

        Description:  Test writing to file for update option.

        Arguments:

        """

        data = None

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.argv_list2.append("-U")
        sys.argv = self.argv_list2

        package_admin.main()

        with open(self.out_file, "r", encoding="UTF-8") as fhdr:
            data = json.load(fhdr)

        self.assertIn("Server", data)

    @mock.patch("package_admin.gen_dnf.Dnf.get_distro")
    @mock.patch("package_admin.gen_dnf.Dnf.fetch_update_pkgs")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_upd_file_json(self, mock_date, mock_host, mock_data,
                                mock_distro):

        """Function:  test_main_upd_file_json

        Description:  Test writing to file in JSON format for update option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.argv_list2.append("-U")
        self.argv_list2.append("-f")
        sys.argv = self.argv_list2

        package_admin.main()

        with open(self.out_file, "r", encoding="UTF-8") as fhdr:
            data = json.load(fhdr)

        self.assertIn("Server", data)

    @mock.patch("package_admin.gen_dnf.Dnf.fetch_update_pkgs")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_upd_sup_std(self, mock_date, mock_host, mock_data):

        """Function:  test_main_upd_sup_std

        Description:  Test suppressing standard out for update option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname

        self.argv_list4.append("-U")
        sys.argv = self.argv_list4

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_dnf.Dnf.fetch_update_pkgs")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_upd_out_std(self, mock_date, mock_host, mock_data):

        """Function:  test_main_upd_out_std

        Description:  Test writing to standard out for update option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname

        self.argv_list5.append("-U")
        sys.argv = self.argv_list5

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_dnf.Dnf.get_distro")
    @mock.patch("package_admin.gen_dnf.Dnf.fetch_install_pkgs")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_ins_file(self, mock_date, mock_host, mock_data, mock_distro):

        """Function:  test_main_ins_file

        Description:  Test writing to file for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.argv_list2.append("-L")
        sys.argv = self.argv_list2

        package_admin.main()

        with open(self.out_file, "r", encoding="UTF-8") as fhdr:
            data = json.load(fhdr)

        self.assertIn("Server", data)

    @mock.patch("package_admin.gen_dnf.Dnf.get_distro")
    @mock.patch("package_admin.gen_dnf.Dnf.fetch_install_pkgs")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_ins_file_json(self, mock_date, mock_host, mock_data,
                                mock_distro):

        """Function:  test_main_ins_file_json

        Description:  Test writing to file in JSON format for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.argv_list2.append("-L")
        self.argv_list2.append("-f")
        sys.argv = self.argv_list2

        package_admin.main()

        with open(self.out_file, "r", encoding="UTF-8") as fhdr:
            data = json.load(fhdr)

        self.assertIn("Server", data)

    @mock.patch("package_admin.gen_dnf.Dnf.fetch_install_pkgs")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_ins_sup_std(self, mock_date, mock_host, mock_data):

        """Function:  test_main_ins_sup_std

        Description:  Test suppressing standard out for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname

        self.argv_list4.append("-L")
        sys.argv = self.argv_list4

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_dnf.Dnf.fetch_install_pkgs")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_ins_out_std(self, mock_date, mock_host, mock_data):

        """Function:  test_main_ins_out_std

        Description:  Test writing to standard out for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname

        self.argv_list5.append("-L")
        sys.argv = self.argv_list5

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_dnf.Dnf.get_distro")
    @mock.patch("package_admin.gen_dnf.Dnf.fetch_repos")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_repo_file(self, mock_date, mock_host, mock_data,
                            mock_distro):

        """Function:  test_main_repo_file

        Description:  Test writing to file for repo option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.argv_list2.append("-R")
        sys.argv = self.argv_list2

        package_admin.main()

        with open(self.out_file, "r", encoding="UTF-8") as fhdr:
            data = json.load(fhdr)

        self.assertIn("Server", data)

    @mock.patch("package_admin.gen_dnf.Dnf.get_distro")
    @mock.patch("package_admin.gen_dnf.Dnf.fetch_repos")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_repo_file_json(self, mock_date, mock_host, mock_data,
                                 mock_distro):

        """Function:  test_main_repo_file_json

        Description:  Test writing to file in JSON format for repo option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.argv_list2.append("-R")
        self.argv_list2.append("-f")
        sys.argv = self.argv_list2

        package_admin.main()

        with open(self.out_file, "r", encoding="UTF-8") as fhdr:
            data = json.load(fhdr)

        self.assertIn("Server", data)

    @mock.patch("package_admin.gen_dnf.Dnf.fetch_repos")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_repo_sup_std(self, mock_date, mock_host, mock_data):

        """Function:  test_main_repo_sup_std

        Description:  Test suppressing standard out for repo option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname

        self.argv_list4.append("-R")
        sys.argv = self.argv_list4

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_dnf.Dnf.fetch_repos")
    @mock.patch("package_admin.gen_dnf.Dnf.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_repo_out_std(self, mock_date, mock_host, mock_data):

        """Function:  test_main_repo_out_std

        Description:  Test writing to standard out for repo option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname

        self.argv_list5.append("-R")
        sys.argv = self.argv_list5

        self.assertFalse(package_admin.main())

    def test_main_arg_dir_chk_crt_false(self):

        """Function:  test_main_arg_dir_chk_crt_false

        Description:  Test for a false directory check.

        Arguments:

        """

        sys.argv = self.argv_list2

        self.assertFalse(package_admin.main())

    def test_main_arg_cond_rep_false(self):

        """Function:  test_main_arg_cond_rep_false

        Description:  Test for a false directory check.

        Arguments:

        """

        sys.argv = self.argv_list2

        with gen_libs.no_std_out():
            self.assertFalse(package_admin.main())

    def test_main_help_func_true(self):

        """Function:  test_main_help_func_true

        Description:  Test for a true help message check.

        Arguments:

        """

        self.argv_list2.append("-h")
        sys.argv = self.argv_list2

        with gen_libs.no_std_out():
            self.assertFalse(package_admin.main())

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:

        """

        if os.path.isfile(self.out_file):
            os.remove(self.out_file)


if __name__ == "__main__":
    unittest.main()
