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


class ArgParser(object):

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
        self.args_array = dict()

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
        self.args2 = ArgParser()
        self.args3 = ArgParser()
        self.args4 = ArgParser()
        self.args2.args_array = {"-e": "ToAddress"}
        self.args3.args_array = {"-e": "ToAddress", "-s": "Subject"}
        self.args4.args_array = {
            "-e": "ToAddress", "-s": "Subject", "-u": True}
        self.data = dict()
        self.mail = Mail()

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

        mock_mail.return_value = self.mail

        self.assertFalse(package_admin.mail_data(self.args2, self.data))

    @mock.patch("package_admin.gen_class.setup_mail")
    def test_mail_subj(self, mock_mail):

        """Function:  test_mailx_data

        Description:  Test with subject option.

        Arguments:

        """

        mock_mail.return_value = self.mail

        self.assertFalse(package_admin.mail_data(self.args3, self.data))

    @mock.patch("package_admin.gen_class.setup_mail")
    def test_mailx_data(self, mock_mail):

        """Function:  test_mailx_data

        Description:  Test with mailx option.

        Arguments:

        """

        mock_mail.return_value = self.mail

        self.assertFalse(package_admin.mail_data(self.args4, self.data))


if __name__ == "__main__":
    unittest.main()
