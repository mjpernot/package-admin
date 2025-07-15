#!/usr/bin/python
# Classification (U)

"""Program:  mail_data.py

    Description:  Unit testing of mail_data in write_file.py.

    Usage:
        test/unit/package_admin/mail_data.py

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


class Mail2():

    """Class:  Mail2

    Description:  Class stub holder for gen_class.Mail2 class.

    Methods:
        __init__
        add_attachment
        send_email

    """

    def __init__(self, subj, to_addr):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.subj = subj
        self.to_addr = to_addr
        self.data = None
        self.fname = None
        self.datatype = None

    def add_attachment(self, fname, datatype, data):

        """Method:  add_attachment

        Description:  Stub method holder for Mail2.add_attachment.

        Arguments:

        """

        self.data = data
        self.fname = fname
        self.datatype = datatype

        return True

    def send_email(self):

        """Method:  send_email

        Description:  Stub method holder for Mail2.send_email.

        Arguments:

        """


class Mail():

    """Class:  Mail

    Description:  Class stub holder for gen_class.Mail class.

    Methods:
        __init__
        add_2_msg
        send_mail

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.data = None

    def add_2_msg(self, data):

        """Method:  add_2_msg

        Description:  Stub method holder for Mail.add_2_msg.

        Arguments:

        """

        self.data = data

        return True

    def send_mail(self, use_mailx=False):

        """Method:  send_mail

        Description:  Stub method holder for Mail.send_mail.

        Arguments:
            (input) use_mailx

        """

        status = True

        if use_mailx:
            status = True

        return status


class ArgParser():

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

    def arg_exist(self, arg):

        """Method:  arg_exist

        Description:  Method stub holder for gen_class.ArgParser.arg_exist.

        Arguments:

        """

        return arg in self.args_array


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_attach_add_hostname
        test_attach_data
        test_no_mail
        test_mail_data
        test_mail_subj
        test_mailx_data

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.data = {}
        self.mail = Mail()
        self.mail2 = Mail2("subj", "to_addr")

    @mock.patch("package_admin.gen_class.Mail2")
    def test_attach_add_hostname(self, mock_mail):

        """Function:  test_attach_add_hostname

        Description:  Test with attaching data and adding hostname to filename.

        Arguments:

        """

        self.args.args_array = {
            "-e": "ToAddress", "-s": "Subject", "-j": "fname_attach",
            "-g": True}

        mock_mail.return_value = self.mail2

        self.assertFalse(package_admin.mail_data(self.args, self.data))

    @mock.patch("package_admin.gen_class.Mail2")
    def test_attach_data(self, mock_mail):

        """Function:  test_attach_data

        Description:  Test with attaching data as an attachment.

        Arguments:

        """

        self.args.args_array = {
            "-e": "ToAddress", "-s": "Subject", "-j": "fname_attach"}

        mock_mail.return_value = self.mail2

        self.assertFalse(package_admin.mail_data(self.args, self.data))

    def test_no_mail(self):

        """Function:  test_no_mail

        Description:  Test with no mail.

        Arguments:

        """

        self.assertFalse(package_admin.mail_data(self.args, self.data))

    @mock.patch("package_admin.gen_class.setup_mail")
    def test_mail_data(self, mock_mail):

        """Function:  test_mail_data

        Description:  Test with mail data.

        Arguments:

        """

        self.args.args_array = {"-e": "ToAddress"}

        mock_mail.return_value = self.mail

        self.assertFalse(package_admin.mail_data(self.args, self.data))

    @mock.patch("package_admin.gen_class.setup_mail")
    def test_mail_subj(self, mock_mail):

        """Function:  test_mailx_data

        Description:  Test with subject option.

        Arguments:

        """

        self.args.args_array = {"-e": "ToAddress", "-s": "Subject"}

        mock_mail.return_value = self.mail

        self.assertFalse(package_admin.mail_data(self.args, self.data))

    @mock.patch("package_admin.gen_class.setup_mail")
    def test_mailx_data(self, mock_mail):

        """Function:  test_mailx_data

        Description:  Test with mailx option.

        Arguments:

        """

        self.args.args_array = {"-e": "ToAddress", "-s": "Subject", "-u": True}

        mock_mail.return_value = self.mail

        self.assertFalse(package_admin.mail_data(self.args, self.data))


if __name__ == "__main__":
    unittest.main()
