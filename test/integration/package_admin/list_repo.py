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
        test_list_repo_file
        test_list_repo_file_json
        test_list_repo_sup_std
        test_list_repo_out_std
        test_list_repo_mongo
        test_list_repo_mongo_file
        tearDown

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

        self.yum = Yum()
        self.base_dir = "test/integration/package_admin"
        self.test_path = os.path.join(os.getcwd(), self.base_dir)
        self.config_path = os.path.join(self.test_path, "config")
        self.mongo_cfg = gen_libs.load_module("mongo", self.config_path)
        self.out_path = os.path.join(self.test_path, "out")
        self.tmp_path = os.path.join(self.test_path, "tmp")
        self.out_file = os.path.join(self.tmp_path, "package_repo.txt")
        self.non_json_file = os.path.join(self.out_path,
                                          "package_repo_non_json")
        self.json_file = os.path.join(self.out_path, "package_repo_json")
        self.dbn = "test_sysmon"
        self.tbl = "test_server_pkgs"
        self.args_array = {"-i": "test_sysmon:test_server_pkgs",
                           "-o": self.out_file, "-z": True}
        self.args_array2 = {"-o": self.out_file, "-z": True}
        self.args_array3 = {"-i": "test_sysmon:test_server_pkgs", "-z": True}
        self.args_array4 = {"-z": True}
        self.args_array5 = {"-z": False}
        self.time_str = "2018-01-01 01:00:00"

    @mock.patch("package_admin.datetime")
    def test_list_repo_file(self, mock_date):

        """Function:  test_list_repo_file

        Description:  Test writing to file.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        package_admin.list_repo(self.args_array2, self.yum,
                                class_cfg=self.mongo_cfg)

        status = filecmp.cmp(self.out_file, self.non_json_file)

        self.assertTrue(status)

    @mock.patch("package_admin.datetime")
    def test_list_repo_file_json(self, mock_date):

        """Function:  test_list_repo_file_json

        Description:  Test writing to file in JSON format.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        self.args_array2["-f"] = True

        package_admin.list_repo(self.args_array2, self.yum,
                                class_cfg=self.mongo_cfg)

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
            package_admin.list_repo(
                self.args_array4, self.yum, class_cfg=self.mongo_cfg),
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
            package_admin.list_repo(
                self.args_array5, self.yum, class_cfg=self.mongo_cfg),
            (True, None))

    @mock.patch("package_admin.datetime")
    def test_list_repo_mongo(self, mock_date):

        """Function:  test_list_repo_mongo

        Description:  Test writing to Mongo database.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        package_admin.list_repo(self.args_array3, self.yum,
                                class_cfg=self.mongo_cfg)

        mongo = mongo_libs.crt_coll_inst(self.mongo_cfg, self.dbn, self.tbl)
        mongo.connect()

        status = \
            True if mongo.coll_find1()["Server"] == self.yum.hostname \
            else False

        mongo_libs.disconnect([mongo])

        self.assertTrue(status)

    @mock.patch("package_admin.datetime")
    def test_list_repo_mongo_file(self, mock_date):

        """Function:  test_list_repo_mongo_file

        Description:  Test writing to Mongo database and to a file.

        Arguments:

        """

        mock_date.datetime.strftime.return_value = self.time_str

        package_admin.list_repo(self.args_array, self.yum,
                                class_cfg=self.mongo_cfg)

        mongo = mongo_libs.crt_coll_inst(self.mongo_cfg, self.dbn, self.tbl)
        mongo.connect()

        if mongo.coll_find1()["Server"] == self.yum.hostname:
            status = filecmp.cmp(self.out_file, self.non_json_file)

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
