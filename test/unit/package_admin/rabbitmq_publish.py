#!/usr/bin/python
# Classification (U)

"""Program:  rabbitmq_publish.py

    Description:  Unit testing of rabbitmq_publish in package_admin.py.

    Usage:
        test/unit/package_admin/rabbitmq_publish.py

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
        test_publish_rabbit_failure
        test_publish_rabbit_successful
        test_no_insert

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.args2 = ArgParser()
        self.args.args_array = {"-r": True, "-b": "rabbitmq", "-d": "config"}
        self.args2.args_array = {"-b": "rabbitmq", "-d": "config"}
        self.data = dict()

        self.status = (True, None)
        self.status2 = (False, "Error Message Here")

        self.results = (True, None)
        self.results2 = (False, "Error Message Here")

    @mock.patch("package_admin.gen_libs.load_module",
                mock.Mock(return_value="cfg"))
    @mock.patch("package_admin.rabbitmq_class.pub_2_rmq")
    def test_publish_rabbit_failure(self, mock_rabbit):

        """Function:  test_publish_rabbit_failure

        Description:  Test with failed publication to RabbitMQ.

        Arguments:

        """

        mock_rabbit.return_value = self.status2

        self.assertEqual(
            package_admin.rabbitmq_publish(
                self.args, self.data), self.results2)

    @mock.patch("package_admin.gen_libs.load_module",
                mock.Mock(return_value="cfg"))
    @mock.patch("package_admin.rabbitmq_class.pub_2_rmq")
    def test_publish_rabbit_successful(self, mock_rabbit):

        """Function:  test_publish_rabbit_successful

        Description:  Test with successful publication to RabbitMQ.

        Arguments:

        """

        mock_rabbit.return_value = self.status

        self.assertEqual(
            package_admin.rabbitmq_publish(self.args, self.data), self.results)

    def test_no_insert(self):

        """Function:  test_no_insert

        Description:  Test with one argument set to False.

        Arguments:

        """

        self.assertEqual(
            package_admin.rabbitmq_publish(
                self.args2, self.data), self.results)


if __name__ == "__main__":
    unittest.main()
