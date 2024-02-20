#!/usr/bin/python
# Classification (U)

"""Program:  display_data.py

    Description:  Unit testing of display_data in write_file.py.

    Usage:
        test/unit/package_admin/display_data.py

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
        test_display_data
        test_suppress_data
        test_default

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.args2 = ArgParser()
        self.args3 = ArgParser()
        self.args2.args_array = {"-z": True}
        self.args3.args_array = {"-z": False}
        self.data = dict()

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    def test_display_data(self):

        """Function:  test_display_data

        Description:  Test with display data to terminal.

        Arguments:

        """

        self.assertFalse(package_admin.display_data(self.args3, self.data))

    def test_suppress_data(self):

        """Function:  test_suppress_data

        Description:  Test with suppressing data.

        Arguments:

        """

        self.assertFalse(package_admin.display_data(self.args2, self.data))

    @mock.patch("package_admin.gen_libs.display_data",
                mock.Mock(return_value=True))
    def test_default(self):

        """Function:  test_default

        Description:  Test with default mode.

        Arguments:

        """

        self.assertFalse(package_admin.display_data(self.args, self.data))


if __name__ == "__main__":
    unittest.main()
