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
        get_args_keys

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = {"-i": "Database_Name:Table_Name"}


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
        test_python_27
        test_python_30

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.dnf = Dnf()
        self.args = ArgParser()
        self.status = (True, None)
        self.status2 = (
            False, "Warning: kernel_run: Only available for Dnf class use")


    @mock.patch("package_admin.kernel_check")
    def test_python_30(self, mock_chk):

        """Function:  test_python_30

        Description:  Test with python 3.0 environment.

        Arguments:

        """

        mock_chk.return_value = self.status, dict()

        self.assertEqual(
            package_admin.kernel_run(self.args, self.dnf), self.status)


if __name__ == "__main__":
    unittest.main()
