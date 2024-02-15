#!/usr/bin/python
# Classification (U)

"""Program:  kernel_run3.py

    Description:  Unit testing of kernel_run in package_admin.py.

    Note:  This is only for Python 3 testing.

    Usage:
        test/unit/package_admin/kernel_run3.py

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
        self.args_array = {"-i": "Database_Name:Table_Name"}

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)


class Dnf(object):

    """Class:  Dnf

    Description:  Class which is a representation of the Dnf class.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the Dnf class.

        Arguments:

        """

        self.host_name = None


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_mongo_rabbit_failure
        test_rabbit_failure
        test_rabbit_successful
        test_mongo_failure
        test_mongo_successful
        test_kernel_failure
        test_kernel_successful
        test_python_30

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.dnf = Dnf()
        self.args = ArgParser()
        self.args.args_array = {"-i": True, "-f": True}
        self.data = {"Server": "ServerName"}

        self.status = (False, "Kernel_Message")
        self.status2 = (True, None)
        self.status3 = (False, "Mongo_Message")
        self.status4 = (False, "Rabbit_Message")

        self.results = (False, "Kernel_Message")
        self.results2 = (True, None)
        self.results3 = (False, "Mongo_Message")
        self.results4 = (False, "Rabbit_Message")
        self.results5 = (False, "Mongo_Message RabbitMQ: Rabbit_Message")

    @mock.patch("package_admin.mail_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.display_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.write_file", mock.Mock(return_value=True))
    @mock.patch("package_admin.rabbitmq_publish")
    @mock.patch("package_admin.mongo_insert")
    @mock.patch("package_admin.kernel_check")
    def test_mongo_rabbit_failure(self, mock_chk, mock_mongo, mock_rabbit):

        """Function:  test_mongo_rabbit_failure

        Description:  Test with mongo insert and rabbitmq publication failure.

        Arguments:

        """

        mock_rabbit.return_value = self.status4
        mock_mongo.return_value = self.status3
        mock_chk.return_value = self.status2, self.data

        self.assertEqual(
            package_admin.kernel_run(self.args, self.dnf), self.results5)

    @mock.patch("package_admin.mail_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.display_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.write_file", mock.Mock(return_value=True))
    @mock.patch("package_admin.rabbitmq_publish")
    @mock.patch("package_admin.mongo_insert")
    @mock.patch("package_admin.kernel_check")
    def test_rabbit_failure(self, mock_chk, mock_mongo, mock_rabbit):

        """Function:  test_rabbit_failure

        Description:  Test with rabbitmq publication failure.

        Arguments:

        """

        mock_rabbit.return_value = self.status4
        mock_mongo.return_value = self.status2
        mock_chk.return_value = self.status2, self.data

        self.assertEqual(
            package_admin.kernel_run(self.args, self.dnf), self.results4)

    @mock.patch("package_admin.mail_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.display_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.write_file", mock.Mock(return_value=True))
    @mock.patch("package_admin.rabbitmq_publish")
    @mock.patch("package_admin.mongo_insert")
    @mock.patch("package_admin.kernel_check")
    def test_rabbit_successful(self, mock_chk, mock_mongo, mock_rabbit):

        """Function:  test_rabbit_successful

        Description:  Test with rabbitmq publication successful.

        Arguments:

        """

        mock_rabbit.return_value = self.status2
        mock_mongo.return_value = self.status2
        mock_chk.return_value = self.status2, self.data

        self.assertEqual(
            package_admin.kernel_run(self.args, self.dnf), self.results2)

    @mock.patch("package_admin.mail_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.display_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.write_file", mock.Mock(return_value=True))
    @mock.patch("package_admin.rabbitmq_publish")
    @mock.patch("package_admin.mongo_insert")
    @mock.patch("package_admin.kernel_check")
    def test_mongo_failure(self, mock_chk, mock_mongo, mock_rabbit):

        """Function:  test_mongo_failure

        Description:  Test with mongo insert failure.

        Arguments:

        """

        mock_rabbit.return_value = self.status2
        mock_mongo.return_value = self.status3
        mock_chk.return_value = self.status2, self.data

        self.assertEqual(
            package_admin.kernel_run(self.args, self.dnf), self.results3)

    @mock.patch("package_admin.mail_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.display_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.write_file", mock.Mock(return_value=True))
    @mock.patch("package_admin.rabbitmq_publish")
    @mock.patch("package_admin.mongo_insert")
    @mock.patch("package_admin.kernel_check")
    def test_mongo_successful(self, mock_chk, mock_mongo, mock_rabbit):

        """Function:  test_mongo_successful

        Description:  Test with mongo insert successful.

        Arguments:

        """

        mock_rabbit.return_value = self.status2
        mock_mongo.return_value = self.status2
        mock_chk.return_value = self.status2, self.data

        self.assertEqual(
            package_admin.kernel_run(self.args, self.dnf), self.results2)

    @mock.patch("package_admin.kernel_check")
    def test_kernel_failure(self, mock_chk):

        """Function:  test_kernel_failure

        Description:  Test with kernel check failure.

        Arguments:

        """

        mock_chk.return_value = self.status, self.data

        self.assertEqual(
            package_admin.kernel_run(self.args, self.dnf), self.results)

    @mock.patch("package_admin.mail_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.display_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.write_file", mock.Mock(return_value=True))
    @mock.patch("package_admin.rabbitmq_publish")
    @mock.patch("package_admin.mongo_insert")
    @mock.patch("package_admin.kernel_check")
    def test_kernel_successful(self, mock_chk, mock_mongo, mock_rabbit):

        """Function:  test_kernel_successful

        Description:  Test with kernel check successful.

        Arguments:

        """

        mock_rabbit.return_value = self.status2
        mock_mongo.return_value = self.status2
        mock_chk.return_value = self.status2, self.data

        self.assertEqual(
            package_admin.kernel_run(self.args, self.dnf), self.results2)

    @mock.patch("package_admin.kernel_check")
    def test_python_30(self, mock_chk):

        """Function:  test_python_30

        Description:  Test with python 3.0 environment.

        Arguments:

        """

        mock_chk.return_value = self.status, dict()

        self.assertEqual(
            package_admin.kernel_run(self.args, self.dnf), self.results2)


if __name__ == "__main__":
    unittest.main()
