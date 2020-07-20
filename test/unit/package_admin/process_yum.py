#!/usr/bin/python
# Classification (U)

"""Program:  process_yum.py

    Description:  Unit testing of process_yum in package_admin.py.

    Usage:
        test/unit/package_admin/process_yum.py

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

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import package_admin
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class Mail(object):

    """Class:  Mail

    Description:  Class stub holder for gen_class.Mail class.

    Methods:
        __init__ -> Class initialization.
        add_2_msg -> add_2_msg method.
        send_mail -> send_mail method.

    """

    def __init__(self, lag_time=1):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.lag_time = lag_time
        self.data = None

    def add_2_msg(self, data):

        """Method:  add_2_msg

        Description:  Stub method holder for Mail.add_2_msg.

        Arguments:

        """

        self.data = data

        return True

    def send_mail(self):

        """Method:  get_name

        Description:  Stub method holder for Mail.send_mail.

        Arguments:

        """

        return True


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Unit testing initilization.
        test_email_json -> Test with email in json format.
        test_email_std -> Test with email in standard format.
        test_mongo_insert -> Test with sending data to Mongo database.
        test_write_file_json -> Test with write to file as formatted JSON.
        test_write_file_true -> Test with write to file is set to True.
        test_suppress_false_json -> Test standard suppression in JSON format.
        test_suppression_false -> Test with standard suppression set to false.
        test_suppression_true -> Test with standard suppression set to true.

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
        self.mail = Mail()
        self.args_array2 = {"-n": True, "-e": "email", "-s": "subj"}
        self.args_array3 = {"-n": True, "-e": "email", "-s": "subj",
                            "-j": True}

    @mock.patch("package_admin.gen_class.setup_mail")
    def test_email_json(self, mock_mail):

        """Function:  test_email_json

        Description:  Test with email in json format.

        Arguments:

        """

        mock_mail.return_value = self.mail

        self.assertFalse(package_admin.process_yum(
            self.args_array3, self.yum, self.dict_key, self.func_name,
            class_cfg=self.class_cfg))

    @mock.patch("package_admin.gen_class.setup_mail")
    def test_email_std(self, mock_mail):

        """Function:  test_email_std

        Description:  Test with email in standard format.

        Arguments:

        """

        mock_mail.return_value = self.mail

        self.assertFalse(package_admin.process_yum(
            self.args_array2, self.yum, self.dict_key, self.func_name,
            class_cfg=self.class_cfg))

    @mock.patch("package_admin.mongo_libs.ins_doc")
    def test_mongo_insert(self, mock_insert):

        """Function:  test_mongo_insert

        Description:  Test with sending data to Mongo database.

        Arguments:

        """

        mock_insert.return_value = True

        self.args_array["-n"] = True

        self.assertFalse(package_admin.process_yum(
            self.args_array, self.yum, self.dict_key, self.func_name,
            class_cfg=self.class_cfg))

    @mock.patch("package_admin.gen_libs.write_file")
    def test_write_file_json(self, mock_write):

        """Function:  test_write_file_json

        Description:  Test with write to file as formatted JSON.

        Arguments:

        """

        mock_write.return_value = True

        self.args_array["-o"] = "File_Name"
        self.args_array["-n"] = True
        self.args_array["-j"] = True

        self.assertFalse(package_admin.process_yum(self.args_array,
                                                   self.yum, self.dict_key,
                                                   self.func_name))

    @mock.patch("package_admin.gen_libs.write_file")
    def test_write_file_true(self, mock_write):

        """Function:  test_write_file_true

        Description:  Test with write to file is set to True.

        Arguments:

        """

        mock_write.return_value = True

        self.args_array["-o"] = "File_Name"
        self.args_array["-n"] = True

        self.assertFalse(package_admin.process_yum(self.args_array,
                                                   self.yum, self.dict_key,
                                                   self.func_name))

    def test_suppress_false_json(self):

        """Function:  test_suppress_false_json

        Description:  Test with standard suppression in JSON format.

        Arguments:

        """

        self.args_array["-j"] = True

        with gen_libs.no_std_out():
            self.assertFalse(package_admin.process_yum(self.args_array,
                                                       self.yum, self.dict_key,
                                                       self.func_name))

    def test_suppression_false(self):

        """Function:  test_suppression_false

        Description:  Test with standard suppression set to false.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(package_admin.process_yum(self.args_array,
                                                       self.yum, self.dict_key,
                                                       self.func_name))

    def test_suppression_true(self):

        """Function:  test_suppression_true

        Description:  Test with standard suppression set to true.

        Arguments:

        """

        self.args_array["-n"] = True

        self.assertFalse(package_admin.process_yum(self.args_array,
                                                   self.yum, self.dict_key,
                                                   self.func_name))


if __name__ == "__main__":
    unittest.main()
