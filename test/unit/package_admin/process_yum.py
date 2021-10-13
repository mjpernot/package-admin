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
import version

__version__ = version.__version__


class Mail(object):

    """Class:  Mail

    Description:  Class stub holder for gen_class.Mail class.

    Methods:
        __init__
        add_2_msg
        send_mail

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

    def send_mail(self, use_mailx=False):

        """Method:  get_name

        Description:  Stub method holder for Mail.send_mail.

        Arguments:
            (input) use_mailx

        """

        status = True

        if use_mailx:
            status = True

        return status


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_append_file_json
        test_append_file
        test_mongo_conn_fail
        test_mongo_conn_success
        test_mailx_json
        test_email_json
        test_mailx_std
        test_email_std
        test_mongo_insert
        test_write_file_json
        test_write_file_true
        test_suppress_false_json
        test_suppression_false
        test_suppression_true

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
                self.data = "Update_Package_List"
                self.distro = ("OS_Name", "Version_Release", "Type_Release")

            def get_distro(self):

                """Method:  get_distro

                Description:  Return self.distro attribute.

                Arguments:
                    (output) self.distro

                """

                return self.distro

            def get_hostname(self):

                """Method:  get_hostname

                Description:  Set self.hostname attribute.

                Arguments:
                    (output) self.hostname

                """

                return self.hostname

            def fetch_update_pkgs(self):

                """Method:  fetch_update_pkgs

                Description:  Set self.data attribute.

                Arguments:
                    (output) self.data

                """

                return self.data

        self.yum = Yum()
        self.args_array = {"-i": "Database_Name:Table_Name"}
        self.class_cfg = "class_cfg_listing"
        self.dict_key = "Update_Packages"
        self.func_name = self.yum.fetch_update_pkgs
        self.mail = Mail()
        self.args_array2 = {"-z": True, "-e": "email", "-s": "subj"}
        self.args_array2a = {"-z": True, "-e": "email", "-s": "subj",
                             "-u": True}
        self.args_array3 = {"-z": True, "-e": "email", "-s": "subj",
                            "-f": True}
        self.args_array3a = {"-z": True, "-e": "email", "-s": "subj",
                             "-f": True, "-u": True}
        self.status = (True, None)
        self.status2 = (False, "Error_Message")
        self.results = (False, "Mongo_Insert: Error_Message")

    @mock.patch("package_admin.gen_libs.write_file")
    def test_append_file_json(self, mock_write):

        """Function:  test_append_file_json

        Description:  Test with append to file as formatted JSON.

        Arguments:

        """

        mock_write.return_value = True

        self.args_array["-o"] = "File_Name"
        self.args_array["-z"] = True
        self.args_array["-f"] = True
        self.args_array["-a"] = True

        self.assertEqual(
            package_admin.process_yum(
                self.args_array, self.yum, self.dict_key, self.func_name),
            self.status)

    @mock.patch("package_admin.gen_libs.write_file")
    def test_append_file(self, mock_write):

        """Function:  test_append_file

        Description:  Test with append to file is set to True.

        Arguments:

        """

        mock_write.return_value = True

        self.args_array["-o"] = "File_Name"
        self.args_array["-z"] = True
        self.args_array["-a"] = True

        self.assertEqual(
            package_admin.process_yum(
                self.args_array, self.yum, self.dict_key, self.func_name),
            self.status)

    @mock.patch("package_admin.mongo_libs.ins_doc")
    def test_mongo_conn_fail(self, mock_insert):

        """Function:  test_mongo_conn_fail

        Description:  Test with failed Mongo connection.

        Arguments:

        """

        mock_insert.return_value = self.status2

        self.args_array["-z"] = True

        self.assertEqual(
            package_admin.process_yum(
                self.args_array, self.yum, self.dict_key, self.func_name,
                class_cfg=self.class_cfg), self.results)

    @mock.patch("package_admin.mongo_libs.ins_doc")
    def test_mongo_conn_success(self, mock_insert):

        """Function:  test_mongo_conn_success

        Description:  Test with successful Mongo connection.

        Arguments:

        """

        mock_insert.return_value = self.status

        self.args_array["-z"] = True

        self.assertEqual(
            package_admin.process_yum(
                self.args_array, self.yum, self.dict_key, self.func_name,
                class_cfg=self.class_cfg), self.status)

    @mock.patch("package_admin.gen_class.setup_mail")
    def test_mailx_json(self, mock_mail):

        """Function:  test_mailx_json

        Description:  Test with mailx in json format.

        Arguments:

        """

        mock_mail.return_value = self.mail

        self.assertEqual(
            package_admin.process_yum(
                self.args_array3a, self.yum, self.dict_key, self.func_name,
                class_cfg=self.class_cfg), self.status)

    @mock.patch("package_admin.gen_class.setup_mail")
    def test_email_json(self, mock_mail):

        """Function:  test_email_json

        Description:  Test with email in json format.

        Arguments:

        """

        mock_mail.return_value = self.mail

        self.assertEqual(
            package_admin.process_yum(
                self.args_array3, self.yum, self.dict_key, self.func_name,
                class_cfg=self.class_cfg), self.status)

    @mock.patch("package_admin.gen_class.setup_mail")
    def test_mailx_std(self, mock_mail):

        """Function:  test_mailx_std

        Description:  Test with mailx in standard format.

        Arguments:

        """

        mock_mail.return_value = self.mail

        self.assertEqual(
            package_admin.process_yum(
                self.args_array2a, self.yum, self.dict_key, self.func_name,
                class_cfg=self.class_cfg), self.status)

    @mock.patch("package_admin.gen_class.setup_mail")
    def test_email_std(self, mock_mail):

        """Function:  test_email_std

        Description:  Test with email in standard format.

        Arguments:

        """

        mock_mail.return_value = self.mail

        self.assertEqual(
            package_admin.process_yum(
                self.args_array2, self.yum, self.dict_key, self.func_name,
                class_cfg=self.class_cfg), self.status)

    @mock.patch("package_admin.mongo_libs.ins_doc")
    def test_mongo_insert(self, mock_insert):

        """Function:  test_mongo_insert

        Description:  Test with sending data to Mongo database.

        Arguments:

        """

        mock_insert.return_value = self.status

        self.args_array["-z"] = True

        self.assertEqual(
            package_admin.process_yum(
                self.args_array, self.yum, self.dict_key, self.func_name,
                class_cfg=self.class_cfg), self.status)

    @mock.patch("package_admin.gen_libs.write_file")
    def test_write_file_json(self, mock_write):

        """Function:  test_write_file_json

        Description:  Test with write to file as formatted JSON.

        Arguments:

        """

        mock_write.return_value = True

        self.args_array["-o"] = "File_Name"
        self.args_array["-z"] = True
        self.args_array["-f"] = True

        self.assertEqual(
            package_admin.process_yum(
                self.args_array, self.yum, self.dict_key, self.func_name),
            self.status)

    @mock.patch("package_admin.gen_libs.write_file")
    def test_write_file_true(self, mock_write):

        """Function:  test_write_file_true

        Description:  Test with write to file is set to True.

        Arguments:

        """

        mock_write.return_value = True

        self.args_array["-o"] = "File_Name"
        self.args_array["-z"] = True

        self.assertEqual(
            package_admin.process_yum(
                self.args_array, self.yum, self.dict_key, self.func_name),
            self.status)

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    def test_suppress_false_json(self):

        """Function:  test_suppress_false_json

        Description:  Test with standard suppression in JSON format.

        Arguments:

        """

        self.args_array["-f"] = True

        self.assertEqual(
            package_admin.process_yum(
                self.args_array, self.yum, self.dict_key, self.func_name),
            self.status)

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    def test_suppression_false(self):

        """Function:  test_suppression_false

        Description:  Test with standard suppression set to false.

        Arguments:

        """

        self.assertEqual(
            package_admin.process_yum(
                self.args_array, self.yum, self.dict_key, self.func_name),
            self.status)

    def test_suppression_true(self):

        """Function:  test_suppression_true

        Description:  Test with standard suppression set to true.

        Arguments:

        """

        self.args_array["-z"] = True

        self.assertEqual(
            package_admin.process_yum(
                self.args_array, self.yum, self.dict_key, self.func_name),
            self.status)


if __name__ == "__main__":
    unittest.main()
