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
        setUp -> Integration testing initilization.
        test_run_program_upd_file -> Test writing to file for update option.
        test_run_program_upd_file_json -> Test writing to file in JSON format
            for update option.
        test_run_program_upd_sup_std -> Test suppressing standard out for
            update option.
        test_run_program_upd_out_std -> Test writing to standard out for update
            option.
        test_run_program_upd_mongo -> Test writing to Mongo database for update
            option.
        test_run_program_upd_mongo_file -> Test writing to Mongo database and
            to a file for update option.
        test_run_program_ins_file -> Test writing to file for install option.
        test_run_program_ins_file_json -> Test writing to file in JSON format
            for install option.
        test_run_program_ins_sup_std -> Test suppressing standard out for
            install option.
        test_run_program_ins_out_std -> Test writing to standard out for
            install option.
        test_run_program_ins_mongo -> Test writing to Mongo database for
            install option.
        test_run_program_ins_mongo_file -> Test writing to Mongo database and
            to a file for install option.
        test_run_program_repo_file -> Test writing to file for repo option.
        test_run_program_repo_file_json -> Test writing to file in JSON format
            for repo option.
        test_run_program_repo_sup_std -> Test suppressing standard out for repo
            option.
        test_run_program_repo_out_std -> Test writing to standard out for repo
            option.
        test_run_program_repo_mongo -> Test writing to Mongo database for repo
            option.
        test_run_program_repo_mongo_file -> Test writing to Mongo database and
            to a file for repo option.
        tearDown -> Clean up of integration testing.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for integration testing.

        Arguments:

        """

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
        self.func_dict = {"-L": package_admin.list_ins_pkg,
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
        self.args_array = {"-i": "test_sysmon:test_server_pkgs",
                           "-o": self.out_file, "-z": True,
                           "-c": "mongo", "-d": self.config_path}
        self.args_array2 = {"-o": self.out_file, "-z": True}
        self.args_array3 = {"-i": "test_sysmon:test_server_pkgs", "-z": True,
                            "-c": "mongo", "-d": self.config_path}
        self.args_array4 = {"-z": True}
        self.args_array5 = {"-z": False}
        self.time_str = "2018-01-01 01:00:00"

    @mock.patch("package_admin.gen_class.Yum.get_distro")
    @mock.patch("package_admin.gen_class.Yum.fetch_update_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_upd_file(self, mock_date, mock_host, mock_data,
                                  mock_distro):

        """Function:  test_run_program_upd_file

        Description:  Test writing to file for update option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.args_array2["-U"] = True

        package_admin.run_program(self.args_array2, self.func_dict)

        status = filecmp.cmp(self.out_file, self.list_non_json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.gen_class.Yum.get_distro")
    @mock.patch("package_admin.gen_class.Yum.fetch_update_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_upd_file_json(self, mock_date, mock_host, mock_data,
                                       mock_distro):

        """Function:  test_run_program_upd_file_json

        Description:  Test writing to file in JSON format for update option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.args_array2["-f"] = True
        self.args_array2["-U"] = True

        package_admin.run_program(self.args_array2, self.func_dict)

        status = filecmp.cmp(self.out_file, self.list_json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.gen_class.Yum.fetch_update_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_upd_sup_std(self, mock_date, mock_host, mock_data):

        """Function:  test_run_program_upd_sup_std

        Description:  Test suppressing standard out for update option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname

        self.args_array4["-U"] = True

        self.assertFalse(package_admin.run_program(self.args_array4,
                                                   self.func_dict))

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_class.Yum.fetch_update_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_upd_out_std(self, mock_date, mock_host, mock_data):

        """Function:  test_run_program_upd_out_std

        Description:  Test writing to standard out for update option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname

        self.args_array5["-U"] = True

        self.assertFalse(package_admin.run_program(self.args_array5,
                                                   self.func_dict))

    @mock.patch("package_admin.gen_class.Yum.fetch_update_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_upd_mongo(self, mock_date, mock_host, mock_data):

        """Function:  test_run_program_upd_mongo

        Description:  Test writing to Mongo database for update option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname

        self.args_array3["-U"] = True

        package_admin.run_program(self.args_array3, self.func_dict)

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
    def test_run_program_upd_mongo_file(self, mock_date, mock_host, mock_data,
                                        mock_distro):

        """Function:  test_run_program_upd_mongo_file

        Description:  Test writing to Mongo database and to a file for update
            option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.upd_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.args_array["-U"] = True

        package_admin.run_program(self.args_array, self.func_dict)

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
    def test_run_program_ins_file(self, mock_date, mock_host, mock_data,
                                  mock_distro):

        """Function:  test_run_program_ins_file

        Description:  Test writing to file for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.args_array2["-L"] = True

        package_admin.run_program(self.args_array2, self.func_dict)

        status = filecmp.cmp(self.out_file, self.ins_non_json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.gen_class.Yum.get_distro")
    @mock.patch("package_admin.gen_class.Yum.fetch_install_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_ins_file_json(self, mock_date, mock_host, mock_data,
                                       mock_distro):

        """Function:  test_run_program_ins_file_json

        Description:  Test writing to file in JSON format for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.args_array2["-f"] = True
        self.args_array2["-L"] = True

        package_admin.run_program(self.args_array2, self.func_dict)

        status = filecmp.cmp(self.out_file, self.ins_json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.gen_class.Yum.fetch_install_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_ins_sup_std(self, mock_date, mock_host, mock_data):

        """Function:  test_run_program_ins_sup_std

        Description:  Test suppressing standard out for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname

        self.args_array4["-L"] = True

        self.assertFalse(package_admin.run_program(self.args_array4,
                                                   self.func_dict))

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_class.Yum.fetch_install_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_ins_out_std(self, mock_date, mock_host, mock_data):

        """Function:  test_run_program_ins_out_std

        Description:  Test writing to standard out for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname

        self.args_array5["-L"] = True

        self.assertFalse(package_admin.run_program(self.args_array5,
                                                   self.func_dict))

    @mock.patch("package_admin.gen_class.Yum.fetch_install_pkgs")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_ins_mongo(self, mock_date, mock_host, mock_data):

        """Function:  test_run_program_ins_mongo

        Description:  Test writing to Mongo database for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname

        self.args_array3["-L"] = True

        package_admin.run_program(self.args_array3, self.func_dict)

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
    def test_run_program_ins_mongo_file(self, mock_date, mock_host, mock_data,
                                        mock_distro):

        """Function:  test_run_program_ins_mongo_file

        Description:  Test writing to Mongo database and to a file for update
            option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.ins_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.args_array["-L"] = True

        package_admin.run_program(self.args_array, self.func_dict)

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
    def test_run_program_repo_file(self, mock_date, mock_host, mock_data,
                                   mock_distro):

        """Function:  test_run_program_repo_file

        Description:  Test writing to file for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.args_array2["-R"] = True

        package_admin.run_program(self.args_array2, self.func_dict)

        status = filecmp.cmp(self.out_file, self.repo_non_json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.gen_class.Yum.get_distro")
    @mock.patch("package_admin.gen_class.Yum.fetch_repos")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_repo_file_json(self, mock_date, mock_host, mock_data,
                                        mock_distro):

        """Function:  test_run_program_repo_file_json

        Description:  Test writing to file in JSON format for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.args_array2["-f"] = True
        self.args_array2["-R"] = True

        package_admin.run_program(self.args_array2, self.func_dict)

        status = filecmp.cmp(self.out_file, self.repo_json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.gen_class.Yum.fetch_repos")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_repo_sup_std(self, mock_date, mock_host, mock_data):

        """Function:  test_run_program_repo_sup_std

        Description:  Test suppressing standard out for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname

        self.args_array4["-R"] = True

        self.assertFalse(package_admin.run_program(self.args_array4,
                                                   self.func_dict))

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_class.Yum.fetch_repos")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_repo_out_std(self, mock_date, mock_host, mock_data):

        """Function:  test_run_program_repo_out_std

        Description:  Test writing to standard out for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname

        self.args_array5["-R"] = True

        self.assertFalse(package_admin.run_program(self.args_array5,
                                                   self.func_dict))

    @mock.patch("package_admin.gen_class.Yum.fetch_repos")
    @mock.patch("package_admin.gen_class.Yum.get_hostname")
    @mock.patch("package_admin.datetime")
    def test_run_program_repo_mongo(self, mock_date, mock_host, mock_data):

        """Function:  test_run_program_repo_mongo

        Description:  Test writing to Mongo database for install option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname

        self.args_array3["-R"] = True

        package_admin.run_program(self.args_array3, self.func_dict)

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
    def test_run_program_repo_mongo_file(self, mock_date, mock_host,
                                         mock_data, mock_distro):

        """Function:  test_run_program_repo_mongo_file

        Description:  Test writing to Mongo database and to a file for update
            option.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str
        mock_data.return_value = self.repo_data
        mock_host.return_value = self.hostname
        mock_distro.return_value = self.distro

        self.args_array["-R"] = True

        package_admin.run_program(self.args_array, self.func_dict)

        mongo = mongo_libs.crt_coll_inst(self.mongo_cfg, self.dbn, self.tbl)
        mongo.connect()

        if mongo.coll_find1()["Server"] == self.hostname:
            status = filecmp.cmp(self.out_file, self.repo_non_json_file)

        else:
            status = False

        mongo_libs.disconnect([mongo])

        self.assertTrue(status)

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
