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
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import package_admin                            # pylint:disable=E0401,C0413
import version                                  # pylint:disable=E0401,C0413

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

        Description:  Initialization instance of the Yum class.

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


class ArgParser(object):                                # pylint:disable=R0903

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        get_val

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = {}

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_rabbitmq_fail
        test_rabbitmq_success
        test_append_file_json
        test_append_file
        test_mailx_json
        test_email_json
        test_mailx_std
        test_email_std
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

        self.yum = Yum()
        self.args = ArgParser()
        self.class_cfg = "class_cfg_listing"
        self.dict_key = "Update_Packages"
        self.func_names = self.yum.fetch_update_pkgs
        self.mail = Mail()

        db_tbl = "Database_Name:Table_Name"
        self.args_array = {"-i": db_tbl}
        self.args_array2 = {"-z": True, "-e": "email", "-s": "subj"}
        self.args_array2a = {
            "-z": True, "-e": "email", "-s": "subj", "-u": True}
        self.args_array3 = {
            "-z": True, "-e": "email", "-s": "subj", "-f": True}
        self.args_array3a = {
            "-z": True, "-e": "email", "-s": "subj", "-f": True, "-u": True}
        self.args_array4 = {
            "-i": db_tbl, "-z": True, "-o": "File_Name", "-f": True,
            "-a": True}
        self.args_array5 = {
            "-i": db_tbl, "-z": True, "-o": "File_Name", "-a": True}
        self.args_array6 = {"-i": db_tbl, "-z": True}
        self.args_array7 = {
            "-i": db_tbl, "-z": True, "-o": "File_Name", "-f": True}
        self.args_array8 = {"-i": db_tbl, "-z": True, "-o": "File_Name"}
        self.args_array9 = {"-i": db_tbl, "-f": True}
        self.args_array10 = {
            "-r": True, "-b": "rmq_config", "-d": "/path/config", "-z": True}
        self.args_array11 = {
            "-r": True, "-b": "rmq_config", "-d": "/path/config", "-z": True,
            "-i": db_tbl}

        self.status = (True, None)
        self.status2 = (False, "Error_Message")
        self.results2 = (False, "RabbitMQ: Error_Message")

    @mock.patch(
        "package_admin.gen_libs.load_module", mock.Mock(return_value=True))
    @mock.patch("package_admin.rabbitmq_class.pub_2_rmq")
    def test_rabbitmq_fail(self, mock_rmq):

        """Function:  test_rabbitmq_fail

        Description:  Test with failed to publish to RabbitMQ.

        Arguments:

        """

        self.args.args_array = self.args_array10

        mock_rmq.return_value = self.status2

        self.assertEqual(
            package_admin.process_yum(
                self.args, self.yum, self.dict_key, self.func_names),
            self.results2)

    @mock.patch(
        "package_admin.gen_libs.load_module", mock.Mock(return_value=True))
    @mock.patch("package_admin.rabbitmq_class.pub_2_rmq")
    def test_rabbitmq_success(self, mock_rmq):

        """Function:  test_rabbitmq_success

        Description:  Test with successful publish to RabbitMQ.

        Arguments:

        """

        self.args.args_array = self.args_array10

        mock_rmq.return_value = self.status

        self.assertEqual(
            package_admin.process_yum(
                self.args, self.yum, self.dict_key, self.func_names),
            self.status)

    @mock.patch("package_admin.gen_libs.write_file")
    def test_append_file_json(self, mock_write):

        """Function:  test_append_file_json

        Description:  Test with append to file as formatted JSON.

        Arguments:

        """

        self.args.args_array = self.args_array4

        mock_write.return_value = True

        self.assertEqual(
            package_admin.process_yum(
                self.args, self.yum, self.dict_key, self.func_names),
            self.status)

    @mock.patch("package_admin.gen_libs.write_file")
    def test_append_file(self, mock_write):

        """Function:  test_append_file

        Description:  Test with append to file is set to True.

        Arguments:

        """

        self.args.args_array = self.args_array5

        mock_write.return_value = True

        self.assertEqual(
            package_admin.process_yum(
                self.args, self.yum, self.dict_key, self.func_names),
            self.status)

    @mock.patch("package_admin.gen_class.setup_mail")
    def test_mailx_json(self, mock_mail):

        """Function:  test_mailx_json

        Description:  Test with mailx in json format.

        Arguments:

        """

        self.args.args_array = self.args_array3a

        mock_mail.return_value = self.mail

        self.assertEqual(
            package_admin.process_yum(
                self.args, self.yum, self.dict_key, self.func_names,
                class_cfg=self.class_cfg), self.status)

    @mock.patch("package_admin.gen_class.setup_mail")
    def test_email_json(self, mock_mail):

        """Function:  test_email_json

        Description:  Test with email in json format.

        Arguments:

        """

        self.args.args_array = self.args_array3

        mock_mail.return_value = self.mail

        self.assertEqual(
            package_admin.process_yum(
                self.args, self.yum, self.dict_key, self.func_names,
                class_cfg=self.class_cfg), self.status)

    @mock.patch("package_admin.gen_class.setup_mail")
    def test_mailx_std(self, mock_mail):

        """Function:  test_mailx_std

        Description:  Test with mailx in standard format.

        Arguments:

        """

        self.args.args_array = self.args_array2a

        mock_mail.return_value = self.mail

        self.assertEqual(
            package_admin.process_yum(
                self.args, self.yum, self.dict_key, self.func_names,
                class_cfg=self.class_cfg), self.status)

    @mock.patch("package_admin.gen_class.setup_mail")
    def test_email_std(self, mock_mail):

        """Function:  test_email_std

        Description:  Test with email in standard format.

        Arguments:

        """

        self.args.args_array = self.args_array2

        mock_mail.return_value = self.mail

        self.assertEqual(
            package_admin.process_yum(
                self.args, self.yum, self.dict_key, self.func_names,
                class_cfg=self.class_cfg), self.status)

    @mock.patch("package_admin.gen_libs.write_file")
    def test_write_file_json(self, mock_write):

        """Function:  test_write_file_json

        Description:  Test with write to file as formatted JSON.

        Arguments:

        """

        self.args.args_array = self.args_array7

        mock_write.return_value = True

        self.assertEqual(
            package_admin.process_yum(
                self.args, self.yum, self.dict_key, self.func_names),
            self.status)

    @mock.patch("package_admin.gen_libs.write_file")
    def test_write_file_true(self, mock_write):

        """Function:  test_write_file_true

        Description:  Test with write to file is set to True.

        Arguments:

        """

        self.args.args_array = self.args_array8

        mock_write.return_value = True

        self.assertEqual(
            package_admin.process_yum(
                self.args, self.yum, self.dict_key, self.func_names),
            self.status)

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    def test_suppress_false_json(self):

        """Function:  test_suppress_false_json

        Description:  Test with standard suppression in JSON format.

        Arguments:

        """

        self.args.args_array = self.args_array9

        self.assertEqual(
            package_admin.process_yum(
                self.args, self.yum, self.dict_key, self.func_names),
            self.status)

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    def test_suppression_false(self):

        """Function:  test_suppression_false

        Description:  Test with standard suppression set to false.

        Arguments:

        """

        self.args.args_array = self.args_array

        self.assertEqual(
            package_admin.process_yum(
                self.args, self.yum, self.dict_key, self.func_names),
            self.status)

    def test_suppression_true(self):

        """Function:  test_suppression_true

        Description:  Test with standard suppression set to true.

        Arguments:

        """

        self.args.args_array = self.args_array6

        self.assertEqual(
            package_admin.process_yum(
                self.args, self.yum, self.dict_key, self.func_names),
            self.status)


if __name__ == "__main__":
    unittest.main()
