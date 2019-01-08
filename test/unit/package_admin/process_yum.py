#!/usr/bin/python
# Classification (U)

"""Program:  process_yum.py

    Description:  Unit testing of process_yum in package_admin.py.

    Usage:
        test/unit/package_admin/process_yum.py

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

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import package_admin
import lib.gen_libs as gen_libs
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
        test_args_array_class_cfg_true_true -> Test first "if" statement for
            true and true.
        test_args_array_class_cfg_true_false -> Test first "if" statement for
            true and false.
        test_args_array_class_cfg_false_true -> Test first "if" statement for
            false and true.
        test_args_array_class_cfg_false_false -> Test first "if" statement for
            false and false.
        test_err_flag_false -> Test err_flag "if" statement as false.
        test_err_flag_true -> Test err_flag "if" statement as true.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:
            None

        """

        class Yum(object):

            """Class:  Yum

            Description:  Class which is a representation of the Yum class.

            Super-Class:  object

            Sub-Classes:  None

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
                        None

                """

                self.hostname = "Server_Host_Name"
                self.data = "Update_Package_List"
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

                Description:  Set self.hostname attribute.

                Arguments:
                    (output) self.hostname -> Server's hostname.

                """

                return self.hostname

            def fetch_update_pkgs(self):

                """Method:  fetch_update_pkgs

                Description:  Set self.data attribute.

                Arguments:
                    (output) self.data -> Server's update package data.

                """

                return self.data

        self.yum = Yum()

        self.args_array = {"-i": "Database_Name:Table_Name"}
        self.class_cfg = "class_cfg_listing"
        self.dict_key = "Update_Packages"
        self.func_name = self.yum.fetch_update_pkgs

    @mock.patch("package_admin.mongo_libs.ins_doc")
    @mock.patch("package_admin.gen_libs.data_multi_out")
    def test_args_array_class_cfg_true_true(self, mock_data, mock_insert):

        """Function:  test_args_array_class_cfg_true_true

        Description:  Test first "if" statement for true and true.

        Arguments:
            mock_data -> Mock Ref:  gen_libs.data_multi_out
            mock_insert -> Mock Ref:  mongo_libs.ins_doc

        """

        # Set mock values.
        mock_data.return_value = (False, None)
        mock_insert.return_value = True

        self.assertFalse(package_admin.process_yum(self.args_array, self.yum,
                                                   self.dict_key,
                                                   self.func_name,
                                                   class_cfg=self.class_cfg))

    @mock.patch("package_admin.gen_libs.data_multi_out")
    def test_args_array_class_cfg_true_false(self, mock_data):

        """Function:  test_args_array_class_cfg_true_false

        Description:  Test first "if" statement for true and false.

        Arguments:
            mock_data -> Mock Ref:  gen_libs.data_multi_out

        """

        # Set mock values.
        mock_data.return_value = (False, None)

        self.assertFalse(package_admin.process_yum(self.args_array, self.yum,
                                                   self.dict_key,
                                                   self.func_name))

    @mock.patch("package_admin.gen_libs.data_multi_out")
    def test_args_array_class_cfg_false_true(self, mock_data):

        """Function:  test_args_array_class_cfg_false_true

        Description:  Test first "if" statement for false and true.

        Arguments:
            mock_data -> Mock Ref:  gen_libs.data_multi_out

        """

        # Set mock values.
        mock_data.return_value = (False, None)

        self.args_array = {"-a": "Database_Name:Table_Name"}

        self.assertFalse(package_admin.process_yum(self.args_array, self.yum,
                                                   self.dict_key,
                                                   self.func_name,
                                                   class_cfg=self.class_cfg))

    @mock.patch("package_admin.gen_libs.data_multi_out")
    def test_args_array_class_cfg_false_false(self, mock_data):

        """Function:  test_args_array_class_cfg_false_false

        Description:  Test first "if" statement for false and false.

        Arguments:
            mock_data -> Mock Ref:  gen_libs.data_multi_out

        """

        # Set mock values.
        mock_data.return_value = (False, None)

        self.args_array = {"-a": "Database_Name:Table_Name"}

        self.assertFalse(package_admin.process_yum(self.args_array, self.yum,
                                                   self.dict_key,
                                                   self.func_name))

    @mock.patch("package_admin.gen_libs.data_multi_out")
    def test_err_flag_false(self, mock_data):

        """Function:  test_err_flag_false

        Description:  Test err_flag "if" statement as false.

        Arguments:
            mock_data -> Mock Ref:  gen_libs.data_multi_out

        """

        # Set mock values.
        mock_data.return_value = (False, None)

        self.assertFalse(package_admin.process_yum(self.args_array, self.yum,
                                                   self.dict_key,
                                                   self.func_name))

    @mock.patch("package_admin.gen_libs.data_multi_out")
    def test_err_flag_true(self, mock_data):

        """Function:  test_err_flag_true

        Description:  Test err_flag "if" statement as true.

        Arguments:
            mock_data -> Mock Ref:  gen_libs.data_multi_out

        """

        # Set mock values.
        mock_data.return_value = (True, "Error_Message_Here")

        with gen_libs.no_std_out():
            self.assertFalse(package_admin.process_yum(self.args_array,
                                                       self.yum, self.dict_key,
                                                       self.func_name))


if __name__ == "__main__":
    unittest.main()
