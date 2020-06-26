#!/usr/bin/python
# Classification (U)

"""Program:  list_ins_pkg.py

    Description:  Integration testing of list_ins_pkg in package_admin.py.

    Usage:
        test/integration/package_admin/list_ins_pkg.py

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

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Integration testing initilization.
        test_list_ins_pkg_file -> Test writing to file.
        test_list_ins_pkg_file_json -> Test writing to file in JSON format.
        test_list_ins_pkg_sup_std -> Test suppressing standard out.
        test_list_ins_pkg_out_std -> Test writing to standard out.
        test_list_ins_pkg_mongo -> Test writing to Mongo database.
        test_list_ins_pkg_mongo_file -> Test writing to Mongo database & file.
        tearDown -> Clean up of integration testing.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class Yum(object):

            """Class:  Yum

            Description:  Class which is a representation of the Yum class.

            Methods:
                __init__ -> Initialize configuration environment.
                get_hostname -> Return Server's hostname.
                get_distro -> Reuturn class' linux_distribution.
                fetch_update_pkgs -> Return Server's update package data.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the Mail class.

                Arguments:

                """

                self.hostname = "Server_Host_Name"
                self.data = {"Package": "PACKAGE_NAME", "Ver": "0.0.0",
                             "Arch": "LINUX"}
                self.distro = ("OS_Name", "Version_Release", "Type_Release")

            def get_distro(self):

                """Method:  get_distro

                Description:  Return self.distro attribute.

                Arguments:
                    (output) self.distro -> Linux distribution tuple value.

                """

                return self.distro

            def get_hostname(self):

                """Method:  get_hostname

                Description:  Return Server's hostname.

                Arguments:
                    (output) self.hostname -> Server's hostname.

                """

                return self.hostname

            def fetch_install_pkgs(self):

                """Method:  fetch_install_pkgs

                Description:  Return Server's update package data.

                Arguments:
                    (output) self.data -> Server's update package data.

                """

                return self.data

        self.yum = Yum()
        self.base_dir = "test/integration/package_admin"
        self.test_path = os.path.join(os.getcwd(), self.base_dir)
        self.config_path = os.path.join(self.test_path, "config")
        self.mongo_cfg = gen_libs.load_module("mongo", self.config_path)
        self.out_path = os.path.join(self.test_path, "out")
        self.out_file = os.path.join(self.out_path, "package_ins_list.txt")
        self.non_json_file = os.path.join(self.out_path,
                                          "package_ins_list_non_json")
        self.json_file = os.path.join(self.out_path, "package_ins_list_json")
        self.db = "test_sysmon"
        self.tbl = "test_server_pkgs"
        self.args_array = {"-i": "test_sysmon:test_server_pkgs",
                           "-o": self.out_file, "-n": True}
        self.args_array2 = {"-o": self.out_file, "-n": True}
        self.args_array3 = {"-i": "test_sysmon:test_server_pkgs", "-n": True}
        self.args_array4 = {"-n": True}
        self.args_array5 = {"-n": False}
        self.time_str = "2018-01-01 01:00:00"

    @mock.patch("package_admin.datetime")
    def test_list_ins_pkg_file(self, mock_date):

        """Function:  test_list_ins_pkg_file

        Description:  Test writing to file.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        package_admin.list_ins_pkg(self.args_array2, self.yum,
                                   class_cfg=self.mongo_cfg)

        status = filecmp.cmp(self.out_file, self.non_json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.datetime")
    def test_list_ins_pkg_file_json(self, mock_date):

        """Function:  test_list_ins_pkg_file_json

        Description:  Test writing to file in JSON format.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        self.args_array2["-j"] = True

        package_admin.list_ins_pkg(self.args_array2, self.yum,
                                   class_cfg=self.mongo_cfg)

        status = filecmp.cmp(self.out_file, self.json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.datetime")
    def test_list_ins_pkg_sup_std(self, mock_date):

        """Function:  test_list_ins_pkg_sup_std

        Description:  Test suppressing standard out.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        self.assertFalse(package_admin.list_ins_pkg(self.args_array4, self.yum,
                                                    class_cfg=self.mongo_cfg))

    @mock.patch("package_admin.datetime")
    def test_list_ins_pkg_out_std(self, mock_date):

        """Function:  test_list_ins_pkg_out_std

        Description:  Test writing to standard out.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        with gen_libs.no_std_out():
            self.assertFalse(package_admin.list_ins_pkg(
                self.args_array5, self.yum, class_cfg=self.mongo_cfg))

    @mock.patch("package_admin.datetime")
    def test_list_ins_pkg_mongo(self, mock_date):

        """Function:  test_list_ins_pkg_mongo

        Description:  Test writing to Mongo database.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        package_admin.list_ins_pkg(self.args_array3, self.yum,
                                   class_cfg=self.mongo_cfg)

        mongo = mongo_libs.crt_coll_inst(self.mongo_cfg, self.db, self.tbl)
        mongo.connect()

        if mongo.coll_find1()["Server"] == self.yum.hostname:
            status = True

        else:
            status = False

        cmds_gen.disconnect([mongo])

        self.assertTrue(status)

    @mock.patch("package_admin.datetime")
    def test_list_ins_pkg_mongo_file(self, mock_date):

        """Function:  test_list_ins_pkg_mongo_file

        Description:  Test writing to Mongo database and to a file.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        package_admin.list_ins_pkg(self.args_array, self.yum,
                                   class_cfg=self.mongo_cfg)

        mongo = mongo_libs.crt_coll_inst(self.mongo_cfg, self.db, self.tbl)
        mongo.connect()

        if mongo.coll_find1()["Server"] == self.yum.hostname:
            status = filecmp.cmp(self.out_file, self.non_json_file)

        else:
            status = False

        cmds_gen.disconnect([mongo])

        self.assertTrue(status)

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of integration testing.

        Arguments:

        """

        mongo = mongo_class.DB(self.mongo_cfg.name, self.mongo_cfg.user,
                               self.mongo_cfg.passwd, self.mongo_cfg.host,
                               self.mongo_cfg.port, self.db,
                               self.mongo_cfg.auth, self.mongo_cfg.conf_file)

        mongo.db_connect(self.db)
        mongo.db_cmd("dropDatabase")
        cmds_gen.disconnect([mongo])

        if os.path.isfile(self.out_file):
            os.remove(self.out_file)


if __name__ == "__main__":
    unittest.main()
