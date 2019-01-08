#!/usr/bin/python
# Classification (U)

"""Program:  main.py

    Description:  Unit testing of main in package_admin.py.

    Usage:
        test/integration/package_admin/main.py

    Arguments:
        None

"""

# Libraries and Global Variables

# Standard
import sys
import os

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import datetime
import filecmp

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import package_admin
import lib.gen_libs as gen_libs
import mongo_lib.mongo_libs as mongo_libs
import mongo_lib.mongo_class as mongo_class
import lib.cmds_gen as cmds_gen

import version

# Version
__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Super-Class:  unittest.TestCase

    Sub-Classes:  None

    Methods:
        setUp -> Unit testing initilization.
        test_main_upd_file -> Test writing to file for update option.
        test_main_upd_file_json -> Test writing to file in JSON format for
            update option.
        test_main_upd_sup_std -> Test suppressing standard out for update
            option.
        test_main_upd_out_std -> Test writing to standard out for update
            option.
        test_main_upd_mongo -> Test writing to Mongo database for update
            option.
        test_main_upd_mongo_file -> Test writing to Mongo database and to a
            file for update option.
        test_main_ins_file -> Test writing to file for install option.
        test_main_ins_file_json -> Test writing to file in JSON format for
            install option.
        test_main_ins_sup_std -> Test suppressing standard out for install
            option.
        test_main_ins_out_std -> Test writing to standard out for install
            option.
        test_main_ins_mongo -> Test writing to Mongo database for install
            option.
        test_main_ins_mongo_file -> Test writing to Mongo database and to a
            file for install option.
        test_main_repo_file -> Test writing to file for repo option.
        test_main_repo_file_json -> Test writing to file in JSON format for
            repo option.
        test_main_repo_sup_std -> Test suppressing standard out for repo
            option.
        test_main_repo_out_std -> Test writing to standard out for repo option.
        test_main_repo_mongo -> Test writing to Mongo database for repo option.
        test_main_repo_mongo_file -> Test writing to Mongo database and to a
            file for repo option.
        test_main_arg_dir_chk_crt_false -> Test for a false directory check.
        test_main_arg_cond_rep_false -> Test for a false directory check.
        test_main_help_func_true -> Test for a true help message check.
        tearDown -> Clean up of integration testing.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for integration testing.

        Arguments:
            None

        """

        self.base_dir = "test/integration/package_admin"
        self.test_path = os.path.join(os.getcwd(), self.base_dir)

        self.config_path = os.path.join(self.test_path, "config")
        self.mongo_cfg = gen_libs.load_module("mongo", self.config_path)

        self.out_path = os.path.join(self.test_path, "out")
        self.out_file = os.path.join(self.out_path, "package_out.txt")

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

        self.db = "test_sysmon"
        self.tbl = "test_server_pkgs"

        self.hostname = "Server_Host_Name"
        self.distro = ("OS_Name", "Version_Release", "Type_Release")
        self.upd_data = {"Package": "PACKAGE_NAME", "Ver": "0.0.0",
                         "Arch": "LINUX", "Repo": "REPO_NAME"}
        self.ins_data = {"Package": "PACKAGE_NAME", "Ver": "0.0.0",
                         "Arch": "LINUX"}
        self.repo_data = ['REPOSITORY_LIST']

        self.argv_list = [os.path.join(self.base_dir, "main.py"),
                          "-i", "test_sysmon:test_server_pkgs",
                          "-o", self.out_file, "-n", "-c", "mongo",
                          "-d", self.config_path]
        self.argv_list2 = [os.path.join(self.base_dir, "main.py"),
                           "-o", self.out_file, "-n"]
        self.argv_list3 = [os.path.join(self.base_dir, "main.py"),
                           "-i", "test_sysmon:test_server_pkgs", "-n",
                           "-c", "mongo", "-d", self.config_path]
        self.argv_list4 = [os.path.join(self.base_dir, "main.py"), "-n"]
        self.argv_list5 = [os.path.join(self.base_dir, "main.py")]

    @mock.patch("package_admin.gen_class.Yum.get_distro")
    @mock.patch("package_admin.gen_class.Yum.fetch_update_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_upd_file(self, mock_date, mock_host, mock_data, mock_distro):

        """Function:  test_main_upd_file

        Description:  Test writing to file for update option.

        Arguments:
            mock_date -> Mock Ref:  package_admin.datetime
            mock_host -> Mock Ref:  package_admin.gen_class.Yum.get_hostname
            mock_data -> Mock Ref:
                package_admin.gen_class.Yum.fetch_update_pkgs
            mock_distro -> Mock Ref:  package_admin.gen_class.Yum.get_distro

        """

        mock_date.datetime.strftime.return_value = "2018-01-01 01:00:00"
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.argv_list2.append("-U")
        sys.argv = self.argv_list2

        package_admin.main()

        status = filecmp.cmp(self.out_file, self.list_non_json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.gen_class.Yum.get_distro")
    @mock.patch("package_admin.gen_class.Yum.fetch_update_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_upd_file_json(self, mock_date, mock_host, mock_data,
                                mock_distro):

        """Function:  test_main_upd_file_json

        Description:  Test writing to file in JSON format for update option.

        Arguments:
            mock_date -> Mock Ref:  package_admin.datetime
            mock_host -> Mock Ref:  package_admin.gen_class.Yum.get_hostname
            mock_data -> Mock Ref:
                package_admin.gen_class.Yum.fetch_update_pkgs
            mock_distro -> Mock Ref:  package_admin.gen_class.Yum.get_distro

        """

        mock_date.datetime.strftime.return_value = "2018-01-01 01:00:00"
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.argv_list2.append("-U")
        self.argv_list2.append("-j")
        sys.argv = self.argv_list2

        package_admin.main()

        status = filecmp.cmp(self.out_file, self.list_json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.gen_class.Yum.fetch_update_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_upd_sup_std(self, mock_date, mock_host, mock_data):

        """Function:  test_main_upd_sup_std

        Description:  Test suppressing standard out for update option.

        Arguments:
            mock_date -> Mock Ref:  package_admin.datetime
            mock_host -> Mock Ref:  package_admin.gen_class.Yum.get_hostname
            mock_data -> Mock Ref:
                package_admin.gen_class.Yum.fetch_update_pkgs

        """

        mock_date.datetime.strftime.return_value = "2018-01-01 01:00:00"
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname

        self.argv_list4.append("-U")
        sys.argv = self.argv_list4

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_class.Yum.fetch_update_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_upd_out_std(self, mock_date, mock_host, mock_data):

        """Function:  test_main_upd_out_std

        Description:  Test writing to standard out for update option.

        Arguments:
            mock_date -> Mock Ref:  package_admin.datetime
            mock_host -> Mock Ref:  package_admin.gen_class.Yum.get_hostname
            mock_data -> Mock Ref:
                package_admin.gen_class.Yum.fetch_update_pkgs

        """

        mock_date.datetime.strftime.return_value = "2018-01-01 01:00:00"
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname

        self.argv_list5.append("-U")
        sys.argv = self.argv_list5

        with gen_libs.no_std_out():
            self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_class.Yum.fetch_update_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_upd_mongo(self, mock_date, mock_host, mock_data):

        """Function:  test_main_upd_mongo

        Description:  Test writing to Mongo database for update option.

        Arguments:
            mock_date -> Mock Ref:  package_admin.datetime
            mock_host -> Mock Ref:  package_admin.gen_class.Yum.get_hostname
            mock_data -> Mock Ref:
                package_admin.gen_class.Yum.fetch_update_pkgs

        """

        mock_date.datetime.strftime.return_value = "2018-01-01 01:00:00"
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname

        self.argv_list3.append("-U")
        sys.argv = self.argv_list3

        package_admin.main()

        COLL = mongo_libs.crt_coll_inst(self.mongo_cfg, self.db, self.tbl)
        COLL.connect()

        if COLL.coll_find1()["Server"] == self.hostname:
            status = True

        else:
            status = False

        cmds_gen.disconnect([COLL])

        self.assertTrue(status)

    @mock.patch("package_admin.gen_class.Yum.get_distro")
    @mock.patch("package_admin.gen_class.Yum.fetch_update_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_upd_mongo_file(self, mock_date, mock_host, mock_data,
                                 mock_distro):

        """Function:  test_main_upd_mongo_file

        Description:  Test writing to Mongo database and to a file for update
            option.

        Arguments:
            mock_date -> Mock Ref:  package_admin.datetime
            mock_host -> Mock Ref:  package_admin.gen_class.Yum.get_hostname
            mock_data -> Mock Ref:
                package_admin.gen_class.Yum.fetch_update_pkgs
            mock_distro -> Mock Ref:  package_admin.gen_class.Yum.get_distro

        """

        mock_date.datetime.strftime.return_value = "2018-01-01 01:00:00"
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.argv_list.append("-U")
        sys.argv = self.argv_list

        package_admin.main()

        COLL = mongo_libs.crt_coll_inst(self.mongo_cfg, self.db, self.tbl)
        COLL.connect()

        if COLL.coll_find1()["Server"] == self.hostname:
            status = filecmp.cmp(self.out_file, self.list_non_json_file)

        else:
            status = False

        cmds_gen.disconnect([COLL])

        self.assertTrue(status)

    @mock.patch("package_admin.gen_class.Yum.get_distro")
    @mock.patch("package_admin.gen_class.Yum.fetch_install_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_ins_file(self, mock_date, mock_host, mock_data, mock_distro):

        """Function:  test_main_ins_file

        Description:  Test writing to file for install option.

        Arguments:
            mock_date -> Mock Ref:  package_admin.datetime
            mock_host -> Mock Ref:  package_admin.gen_class.Yum.get_hostname
            mock_data -> Mock Ref:
                package_admin.gen_class.Yum.fetch_install_pkgs
            mock_distro -> Mock Ref:  package_admin.gen_class.Yum.get_distro

        """

        mock_date.datetime.strftime.return_value = "2018-01-01 01:00:00"
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.argv_list2.append("-L")
        sys.argv = self.argv_list2

        package_admin.main()

        status = filecmp.cmp(self.out_file, self.ins_non_json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.gen_class.Yum.get_distro")
    @mock.patch("package_admin.gen_class.Yum.fetch_install_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_ins_file_json(self, mock_date, mock_host, mock_data,
                                mock_distro):

        """Function:  test_main_ins_file_json

        Description:  Test writing to file in JSON format for install option.

        Arguments:
            mock_date -> Mock Ref:  package_admin.datetime
            mock_host -> Mock Ref:  package_admin.gen_class.Yum.get_hostname
            mock_data -> Mock Ref:
                package_admin.gen_class.Yum.fetch_install_pkgs
            mock_distro -> Mock Ref:  package_admin.gen_class.Yum.get_distro

        """

        mock_date.datetime.strftime.return_value = "2018-01-01 01:00:00"
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.argv_list2.append("-L")
        self.argv_list2.append("-j")
        sys.argv = self.argv_list2

        package_admin.main()

        status = filecmp.cmp(self.out_file, self.ins_json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.gen_class.Yum.fetch_install_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_ins_sup_std(self, mock_date, mock_host, mock_data):

        """Function:  test_main_ins_sup_std

        Description:  Test suppressing standard out for install option.

        Arguments:
            mock_date -> Mock Ref:  package_admin.datetime
            mock_host -> Mock Ref:  package_admin.gen_class.Yum.get_hostname
            mock_data -> Mock Ref:
                package_admin.gen_class.Yum.fetch_install_pkgs

        """

        mock_date.datetime.strftime.return_value = "2018-01-01 01:00:00"
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname

        self.argv_list4.append("-L")
        sys.argv = self.argv_list4

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_class.Yum.fetch_install_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_ins_out_std(self, mock_date, mock_host, mock_data):

        """Function:  test_main_ins_out_std

        Description:  Test writing to standard out for install option.

        Arguments:
            mock_date -> Mock Ref:  package_admin.datetime
            mock_host -> Mock Ref:  package_admin.gen_class.Yum.get_hostname
            mock_data -> Mock Ref:
                package_admin.gen_class.Yum.fetch_install_pkgs

        """

        mock_date.datetime.strftime.return_value = "2018-01-01 01:00:00"
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname

        self.argv_list5.append("-L")
        sys.argv = self.argv_list5

        with gen_libs.no_std_out():
            self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_class.Yum.fetch_install_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_ins_mongo(self, mock_date, mock_host, mock_data):

        """Function:  test_main_ins_mongo

        Description:  Test writing to Mongo database for install option.

        Arguments:
            mock_date -> Mock Ref:  package_admin.datetime
            mock_host -> Mock Ref:  package_admin.gen_class.Yum.get_hostname
            mock_data -> Mock Ref:
                package_admin.gen_class.Yum.fetch_install_pkgs

        """

        mock_date.datetime.strftime.return_value = "2018-01-01 01:00:00"
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname

        self.argv_list3.append("-L")
        sys.argv = self.argv_list3

        package_admin.main()

        COLL = mongo_libs.crt_coll_inst(self.mongo_cfg, self.db, self.tbl)
        COLL.connect()

        if COLL.coll_find1()["Server"] == self.hostname:
            status = True

        else:
            status = False

        cmds_gen.disconnect([COLL])

        self.assertTrue(status)

    @mock.patch("package_admin.gen_class.Yum.get_distro")
    @mock.patch("package_admin.gen_class.Yum.fetch_install_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_ins_mongo_file(self, mock_date, mock_host, mock_data,
                                 mock_distro):

        """Function:  test_main_ins_mongo_file

        Description:  Test writing to Mongo database and to a file for install
            option.

        Arguments:
            mock_date -> Mock Ref:  package_admin.datetime
            mock_host -> Mock Ref:  package_admin.gen_class.Yum.get_hostname
            mock_data -> Mock Ref:
                package_admin.gen_class.Yum.fetch_install_pkgs
            mock_distro -> Mock Ref:  package_admin.gen_class.Yum.get_distro

        """

        mock_date.datetime.strftime.return_value = "2018-01-01 01:00:00"
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.argv_list.append("-L")
        sys.argv = self.argv_list

        package_admin.main()

        COLL = mongo_libs.crt_coll_inst(self.mongo_cfg, self.db, self.tbl)
        COLL.connect()

        if COLL.coll_find1()["Server"] == self.hostname:
            status = filecmp.cmp(self.out_file, self.ins_non_json_file)

        else:
            status = False

        cmds_gen.disconnect([COLL])

        self.assertTrue(status)

    @mock.patch("package_admin.gen_class.Yum.get_distro")
    @mock.patch("package_admin.gen_class.Yum.fetch_repos")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_repo_file(self, mock_date, mock_host, mock_data,
                            mock_distro):

        """Function:  test_main_repo_file

        Description:  Test writing to file for repo option.

        Arguments:
            mock_date -> Mock Ref:  package_admin.datetime
            mock_host -> Mock Ref:  package_admin.gen_class.Yum.get_hostname
            mock_data -> Mock Ref:  package_admin.gen_class.Yum.fetch_repos
            mock_distro -> Mock Ref:  package_admin.gen_class.Yum.get_distro

        """

        mock_date.datetime.strftime.return_value = "2018-01-01 01:00:00"
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.argv_list2.append("-R")
        sys.argv = self.argv_list2

        package_admin.main()

        status = filecmp.cmp(self.out_file, self.repo_non_json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.gen_class.Yum.get_distro")
    @mock.patch("package_admin.gen_class.Yum.fetch_repos")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_repo_file_json(self, mock_date, mock_host, mock_data,
                                 mock_distro):

        """Function:  test_main_repo_file_json

        Description:  Test writing to file in JSON format for repo option.

        Arguments:
            mock_date -> Mock Ref:  package_admin.datetime
            mock_host -> Mock Ref:  package_admin.gen_class.Yum.get_hostname
            mock_data -> Mock Ref:  package_admin.gen_class.Yum.fetch_repos
            mock_distro -> Mock Ref:  package_admin.gen_class.Yum.get_distro

        """

        mock_date.datetime.strftime.return_value = "2018-01-01 01:00:00"
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.argv_list2.append("-R")
        self.argv_list2.append("-j")
        sys.argv = self.argv_list2

        package_admin.main()

        status = filecmp.cmp(self.out_file, self.repo_json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.gen_class.Yum.fetch_repos")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_repo_sup_std(self, mock_date, mock_host, mock_data):

        """Function:  test_main_repo_sup_std

        Description:  Test suppressing standard out for repo option.

        Arguments:
            mock_date -> Mock Ref:  package_admin.datetime
            mock_host -> Mock Ref:  package_admin.gen_class.Yum.get_hostname
            mock_data -> Mock Ref:  package_admin.gen_class.Yum.fetch_repos

        """

        mock_date.datetime.strftime.return_value = "2018-01-01 01:00:00"
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname

        self.argv_list4.append("-R")
        sys.argv = self.argv_list4

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_class.Yum.fetch_repos")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_repo_out_std(self, mock_date, mock_host, mock_data):

        """Function:  test_main_repo_out_std

        Description:  Test writing to standard out for repo option.

        Arguments:
            mock_date -> Mock Ref:  package_admin.datetime
            mock_host -> Mock Ref:  package_admin.gen_class.Yum.get_hostname
            mock_data -> Mock Ref:  package_admin.gen_class.Yum.fetch_repos

        """

        mock_date.datetime.strftime.return_value = "2018-01-01 01:00:00"
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname

        self.argv_list5.append("-R")
        sys.argv = self.argv_list5

        with gen_libs.no_std_out():
            self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_class.Yum.fetch_repos")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_repo_mongo(self, mock_date, mock_host, mock_data):

        """Function:  test_main_repo_mongo

        Description:  Test writing to Mongo database for repo option.

        Arguments:
            mock_date -> Mock Ref:  package_admin.datetime
            mock_host -> Mock Ref:  package_admin.gen_class.Yum.get_hostname
            mock_data -> Mock Ref:  package_admin.gen_class.Yum.fetch_repos

        """

        mock_date.datetime.strftime.return_value = "2018-01-01 01:00:00"
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname

        self.argv_list3.append("-R")
        sys.argv = self.argv_list3

        package_admin.main()

        COLL = mongo_libs.crt_coll_inst(self.mongo_cfg, self.db, self.tbl)
        COLL.connect()

        if COLL.coll_find1()["Server"] == self.hostname:
            status = True

        else:
            status = False

        cmds_gen.disconnect([COLL])

        self.assertTrue(status)

    @mock.patch("package_admin.gen_class.Yum.get_distro")
    @mock.patch("package_admin.gen_class.Yum.fetch_repos")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_repo_mongo_file(self, mock_date, mock_host, mock_data,
                                  mock_distro):

        """Function:  test_main_repo_mongo_file

        Description:  Test writing to Mongo database and to a file for repo
            option.

        Arguments:
            mock_date -> Mock Ref:  package_admin.datetime
            mock_host -> Mock Ref:  package_admin.gen_class.Yum.get_hostname
            mock_data -> Mock Ref:  package_admin.gen_class.Yum.fetch_repos
            mock_distro -> Mock Ref:  package_admin.gen_class.Yum.get_distro

        """

        mock_date.datetime.strftime.return_value = "2018-01-01 01:00:00"
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.argv_list.append("-R")
        sys.argv = self.argv_list

        package_admin.main()

        COLL = mongo_libs.crt_coll_inst(self.mongo_cfg, self.db, self.tbl)
        COLL.connect()

        if COLL.coll_find1()["Server"] == self.hostname:
            status = filecmp.cmp(self.out_file, self.repo_non_json_file)

        else:
            status = False

        cmds_gen.disconnect([COLL])

        self.assertTrue(status)

    def test_main_arg_dir_chk_crt_false(self):

        """Function:  test_main_arg_dir_chk_crt_false

        Description:  Test for a false directory check.

        Arguments:
            None

        """

        self.config_path = os.path.join(self.test_path, "bad_config")
        self.argv_list2.append("-c")
        self.argv_list2.append("mongo")
        self.argv_list2.append("-d")
        self.argv_list2.append(self.config_path)
        sys.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(package_admin.main())

    def test_main_arg_cond_rep_false(self):

        """Function:  test_main_arg_cond_rep_false

        Description:  Test for a false directory check.

        Arguments:
            None

        """

        self.argv_list2.append("-c")
        self.argv_list2.append("mongo")
        sys.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(package_admin.main())

    def test_main_help_func_true(self):

        """Function:  test_main_help_func_true

        Description:  Test for a true help message check.

        Arguments:
            None

        """

        self.argv_list2.append("-h")
        sys.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(package_admin.main())

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:
            None

        """

        DB = mongo_class.DB(self.mongo_cfg.name, self.mongo_cfg.user,
                            self.mongo_cfg.passwd, self.mongo_cfg.host,
                            self.mongo_cfg.port, self.db, self.mongo_cfg.auth,
                            self.mongo_cfg.conf_file)

        DB.db_connect(self.db)
        DB.db_cmd("dropDatabase")
        cmds_gen.disconnect([DB])

        if os.path.isfile(self.out_file):
            os.remove(self.out_file)


if __name__ == "__main__":
    unittest.main()
