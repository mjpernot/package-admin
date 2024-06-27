#!/usr/bin/python
# Classification (U)

"""Program:  output_run.py

    Description:  Unit testing of output_run in package_admin.py.

    Note:  This is only for Python 3 testing.

    Usage:
        test/unit/package_admin/output_run.py

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

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.args2 = ArgParser()
        self.args.args_array = {"-i": True, "-f": True}
        self.data = {"Server": "ServerName"}

        self.status2 = (True, None)
        self.status3 = (False, "Mongo_Message")
        self.status4 = (False, "Rabbit_Message")

        self.results2 = (True, None)
        self.results3 = (False, "Mongo_Message")
        self.results4 = (False, "Rabbit_Message")
        self.results5 = (
            False, "MongoDB: Mongo_Message RabbitMQ: Rabbit_Message")

    @mock.patch("package_admin.mail_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.display_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.write_file", mock.Mock(return_value=True))
    @mock.patch("package_admin.rabbitmq_publish")
    @mock.patch("package_admin.mongo_insert")
    def test_mongo_rabbit_failure(self, mock_mongo, mock_rabbit):

        """Function:  test_mongo_rabbit_failure

        Description:  Test with mongo insert and rabbitmq publication failure.

        Arguments:

        """

        mock_rabbit.return_value = self.status4
        mock_mongo.return_value = self.status3

        self.assertEqual(
            package_admin.output_run(self.args, self.data), self.results5)

    @mock.patch("package_admin.mail_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.display_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.write_file", mock.Mock(return_value=True))
    @mock.patch("package_admin.rabbitmq_publish")
    @mock.patch("package_admin.mongo_insert")
    def test_rabbit_failure(self, mock_mongo, mock_rabbit):

        """Function:  test_rabbit_failure

        Description:  Test with rabbitmq publication failure.

        Arguments:

        """

        mock_rabbit.return_value = self.status4
        mock_mongo.return_value = self.status2

        self.assertEqual(
            package_admin.output_run(self.args, self.data), self.results4)

    @mock.patch("package_admin.mail_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.display_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.write_file", mock.Mock(return_value=True))
    @mock.patch("package_admin.rabbitmq_publish")
    @mock.patch("package_admin.mongo_insert")
    def test_rabbit_successful(self, mock_mongo, mock_rabbit):

        """Function:  test_rabbit_successful

        Description:  Test with rabbitmq publication successful.

        Arguments:

        """

        mock_rabbit.return_value = self.status2
        mock_mongo.return_value = self.status2

        self.assertEqual(
            package_admin.output_run(self.args, self.data), self.results2)

    @mock.patch("package_admin.mail_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.display_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.write_file", mock.Mock(return_value=True))
    @mock.patch("package_admin.rabbitmq_publish")
    @mock.patch("package_admin.mongo_insert")
    def test_mongo_failure(self, mock_mongo, mock_rabbit):

        """Function:  test_mongo_failure

        Description:  Test with mongo insert failure.

        Arguments:

        """

        mock_rabbit.return_value = self.status2
        mock_mongo.return_value = self.status3

        self.assertEqual(
            package_admin.output_run(self.args, self.data), self.results3)

    @mock.patch("package_admin.mail_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.display_data", mock.Mock(return_value=True))
    @mock.patch("package_admin.write_file", mock.Mock(return_value=True))
    @mock.patch("package_admin.rabbitmq_publish")
    @mock.patch("package_admin.mongo_insert")
    def test_mongo_successful(self, mock_mongo, mock_rabbit):

        """Function:  test_mongo_successful

        Description:  Test with mongo insert successful.

        Arguments:

        """

        mock_rabbit.return_value = self.status2
        mock_mongo.return_value = self.status2

        self.assertEqual(
            package_admin.output_run(self.args, self.data), self.results2)


if __name__ == "__main__":
    unittest.main()
