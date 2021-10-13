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

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import filecmp

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import package_admin
import lib.gen_libs as gen_libs
import mongo_lib.mongo_libs as mongo_libs
import mongo_lib.mongo_class as mongo_class

import version

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
        test_main_upd_mongo
        test_main_upd_mongo_file
        test_main_ins_file
        test_main_ins_file_json
        test_main_ins_sup_std
        test_main_ins_out_std
        test_main_ins_mongo
        test_main_ins_mongo_file
        test_main_repo_file
        test_main_repo_file_json
        test_main_repo_sup_std
        test_main_repo_out_std
        test_main_repo_mongo
        test_main_repo_mongo_file
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
        self.config_path = os.path.join(self.test_path, "config")
        self.mongo_cfg = gen_libs.load_module("mongo", self.config_path)
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
        self.dbn = "test_sysmon"
        self.tbl = "test_server_pkgs"
        self.hostname = "Server_Host_Name"
        self.distro = ("OS_Name", "Version_Release", "Type_Release")
        self.upd_data = {"Package": "PACKAGE_NAME", "Ver": "0.0.0",
                         "Arch": "LINUX", "Repo": "REPO_NAME"}
        self.ins_data = {"Package": "PACKAGE_NAME", "Ver": "0.0.0",
                         "Arch": "LINUX"}
        self.repo_data = ['REPOSITORY_LIST']
        self.argv_list = [os.path.join(self.base_dir, self.main),
                          "-i", "test_sysmon:test_server_pkgs",
                          "-o", self.out_file, "-z", "-c", "mongo",
                          "-d", self.config_path]
        self.argv_list2 = [os.path.join(self.base_dir, self.main),
                           "-o", self.out_file, "-z"]
        self.argv_list3 = [os.path.join(self.base_dir, self.main),
                           "-i", "test_sysmon:test_server_pkgs", "-z",
                           "-c", "mongo", "-d", self.config_path]
        self.argv_list4 = [os.path.join(self.base_dir, self.main), "-z"]
        self.argv_list5 = [os.path.join(self.base_dir, self.main)]
        self.time_str = "2018-01-01 01:00:00"

    @mock.patch("package_admin.gen_class.Yum.get_distro")
    @mock.patch("package_admin.gen_class.Yum.fetch_update_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_upd_file(self, mock_date, mock_host, mock_data, mock_distro):

        """Function:  test_main_upd_file

        Description:  Test writing to file for update option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        cmdline = gen_libs.get_inst(sys)
        self.argv_list2.append("-U")
        cmdline.argv = self.argv_list2

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

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        cmdline = gen_libs.get_inst(sys)
        self.argv_list2.append("-U")
        self.argv_list2.append("-f")
        cmdline.argv = self.argv_list2

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

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname

        cmdline = gen_libs.get_inst(sys)
        self.argv_list4.append("-U")
        cmdline.argv = self.argv_list4

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_class.Yum.fetch_update_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_upd_out_std(self, mock_date, mock_host, mock_data):

        """Function:  test_main_upd_out_std

        Description:  Test writing to standard out for update option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname

        cmdline = gen_libs.get_inst(sys)
        self.argv_list5.append("-U")
        cmdline.argv = self.argv_list5

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_class.Yum.fetch_update_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_upd_mongo(self, mock_date, mock_host, mock_data):

        """Function:  test_main_upd_mongo

        Description:  Test writing to Mongo database for update option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname

        cmdline = gen_libs.get_inst(sys)
        self.argv_list3.append("-U")
        cmdline.argv = self.argv_list3

        package_admin.main()

        mongo = mongo_libs.crt_coll_inst(self.mongo_cfg, self.dbn, self.tbl)
        mongo.connect()

        status = \
            True if mongo.coll_find1()["Server"] == self.hostname else False

        mongo_libs.disconnect([mongo])

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

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        cmdline = gen_libs.get_inst(sys)
        self.argv_list.append("-U")
        cmdline.argv = self.argv_list

        package_admin.main()

        mongo = mongo_libs.crt_coll_inst(self.mongo_cfg, self.dbn, self.tbl)
        mongo.connect()

        if mongo.coll_find1()["Server"] == self.hostname:
            status = filecmp.cmp(self.out_file, self.list_non_json_file)

        else:
            status = False

        mongo_libs.disconnect([mongo])

        self.assertTrue(status)

    @mock.patch("package_admin.gen_class.Yum.get_distro")
    @mock.patch("package_admin.gen_class.Yum.fetch_install_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
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

        cmdline = gen_libs.get_inst(sys)
        self.argv_list2.append("-L")
        cmdline.argv = self.argv_list2

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

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        cmdline = gen_libs.get_inst(sys)
        self.argv_list2.append("-L")
        self.argv_list2.append("-f")
        cmdline.argv = self.argv_list2

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

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname

        cmdline = gen_libs.get_inst(sys)
        self.argv_list4.append("-L")
        cmdline.argv = self.argv_list4

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_class.Yum.fetch_install_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_ins_out_std(self, mock_date, mock_host, mock_data):

        """Function:  test_main_ins_out_std

        Description:  Test writing to standard out for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname

        cmdline = gen_libs.get_inst(sys)
        self.argv_list5.append("-L")
        cmdline.argv = self.argv_list5

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_class.Yum.fetch_install_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_ins_mongo(self, mock_date, mock_host, mock_data):

        """Function:  test_main_ins_mongo

        Description:  Test writing to Mongo database for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname

        cmdline = gen_libs.get_inst(sys)
        self.argv_list3.append("-L")
        cmdline.argv = self.argv_list3

        package_admin.main()

        mongo = mongo_libs.crt_coll_inst(self.mongo_cfg, self.dbn, self.tbl)
        mongo.connect()

        status = \
            True if mongo.coll_find1()["Server"] == self.hostname else False

        mongo_libs.disconnect([mongo])

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

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        cmdline = gen_libs.get_inst(sys)
        self.argv_list.append("-L")
        cmdline.argv = self.argv_list

        package_admin.main()

        mongo = mongo_libs.crt_coll_inst(self.mongo_cfg, self.dbn, self.tbl)
        mongo.connect()

        if mongo.coll_find1()["Server"] == self.hostname:
            status = filecmp.cmp(self.out_file, self.ins_non_json_file)

        else:
            status = False

        mongo_libs.disconnect([mongo])

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

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        cmdline = gen_libs.get_inst(sys)
        self.argv_list2.append("-R")
        cmdline.argv = self.argv_list2

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

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        cmdline = gen_libs.get_inst(sys)
        self.argv_list2.append("-R")
        self.argv_list2.append("-f")
        cmdline.argv = self.argv_list2

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

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname

        cmdline = gen_libs.get_inst(sys)
        self.argv_list4.append("-R")
        cmdline.argv = self.argv_list4

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_class.Yum.fetch_repos")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_repo_out_std(self, mock_date, mock_host, mock_data):

        """Function:  test_main_repo_out_std

        Description:  Test writing to standard out for repo option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname

        cmdline = gen_libs.get_inst(sys)
        self.argv_list5.append("-R")
        cmdline.argv = self.argv_list5

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_class.Yum.fetch_repos")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_main_repo_mongo(self, mock_date, mock_host, mock_data):

        """Function:  test_main_repo_mongo

        Description:  Test writing to Mongo database for repo option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname

        cmdline = gen_libs.get_inst(sys)
        self.argv_list3.append("-R")
        cmdline.argv = self.argv_list3

        package_admin.main()

        mongo = mongo_libs.crt_coll_inst(self.mongo_cfg, self.dbn, self.tbl)
        mongo.connect()

        status = \
            True if mongo.coll_find1()["Server"] == self.hostname else False

        mongo_libs.disconnect([mongo])

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

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        cmdline = gen_libs.get_inst(sys)
        self.argv_list.append("-R")
        cmdline.argv = self.argv_list

        package_admin.main()

        mongo = mongo_libs.crt_coll_inst(self.mongo_cfg, self.dbn, self.tbl)
        mongo.connect()

        if mongo.coll_find1()["Server"] == self.hostname:
            status = filecmp.cmp(self.out_file, self.repo_non_json_file)

        else:
            status = False

        mongo_libs.disconnect([mongo])

        self.assertTrue(status)

    def test_main_arg_dir_chk_crt_false(self):

        """Function:  test_main_arg_dir_chk_crt_false

        Description:  Test for a false directory check.

        Arguments:

        """

        cmdline = gen_libs.get_inst(sys)
        self.config_path = os.path.join(self.test_path, "bad_config")
        self.argv_list2.append("-c")
        self.argv_list2.append("mongo")
        self.argv_list2.append("-d")
        self.argv_list2.append(self.config_path)
        cmdline.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(package_admin.main())

    def test_main_arg_cond_rep_false(self):

        """Function:  test_main_arg_cond_rep_false

        Description:  Test for a false directory check.

        Arguments:

        """

        cmdline = gen_libs.get_inst(sys)
        self.argv_list2.append("-c")
        self.argv_list2.append("mongo")
        cmdline.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(package_admin.main())

    def test_main_help_func_true(self):

        """Function:  test_main_help_func_true

        Description:  Test for a true help message check.

        Arguments:

        """

        cmdline = gen_libs.get_inst(sys)
        self.argv_list2.append("-h")
        cmdline.argv = self.argv_list

        with gen_libs.no_std_out():
            self.assertFalse(package_admin.main())

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:

        """

        mongo = mongo_class.DB(
            self.mongo_cfg.name, self.mongo_cfg.user, self.mongo_cfg.japd,
            self.mongo_cfg.host, self.mongo_cfg.port, db=self.dbn,
            auth=self.mongo_cfg.auth, conf_file=self.mongo_cfg.conf_file)

        mongo.db_connect(self.dbn)
        mongo.db_cmd("dropDatabase")
        mongo_libs.disconnect([mongo])

        if os.path.isfile(self.out_file):
            os.remove(self.out_file)


if __name__ == "__main__":
    unittest.main()
