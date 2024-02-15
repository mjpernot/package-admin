#!/usr/bin/python
# Classification (U)

"""Program:  write_file.py

    Description:  Unit testing of rabbitmq_publish in write_file.py.

    Usage:
        test/unit/package_admin/write_file.py

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
        test_write_file_write
        test_write_file_append
        test_write_file_default
        test_no_write_file

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
        self.args.args_array = {"-o": "FileName", "-a": "w"}
        self.args2.args_array = {"-o": "FileName", "-a": "a"}
        self.args3.args_array = {"-o": "FileName"}
        self.args4.args_array = {"-a": "a"}
        self.data = dict()

    @mock.patch("package_admin.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_write_file_write(self):

        """Function:  test_write_file_write

        Description:  Test with writing to file with write mode.

        Arguments:

        """

        self.assertFalse(package_admin.write_file(self.args, self.data))

    @mock.patch("package_admin.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_write_file_append(self):

        """Function:  test_write_file_append

        Description:  Test with writing to file with append mode.

        Arguments:

        """

        self.assertFalse(package_admin.write_file(self.args2, self.data))

    @mock.patch("package_admin.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_write_file_default(self):

        """Function:  test_write_file_default

        Description:  Test with writing to file with default mode.

        Arguments:

        """

        self.assertFalse(package_admin.write_file(self.args3, self.data))

    @mock.patch("package_admin.gen_libs.write_file",
                mock.Mock(return_value=True))
    def test_no_write_file(self):

        """Function:  test_no_write_file

        Description:  Test with no writing to file.

        Arguments:

        """

        self.assertFalse(package_admin.write_file(self.args4, self.data))


if __name__ == "__main__":
    unittest.main()
