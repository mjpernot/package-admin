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
import package_admin                            # pylint:disable=E0401,C0413
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class ArgParser(object):                                # pylint:disable=R0903

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = {"-i": "Database_Name:Table_Name"}


class Dnf(object):                                      # pylint:disable=R0903

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

        self.results = (False, "Kernel_Message")
        self.results2 = (True, None)

    @mock.patch("package_admin.kernel_check")
    def test_kernel_failure(self, mock_chk):

        """Function:  test_kernel_failure

        Description:  Test with kernel check failure.

        Arguments:

        """

        mock_chk.return_value = self.status, self.data

        self.assertEqual(
            package_admin.kernel_run(self.args, self.dnf), self.results)

    @mock.patch("package_admin.output_run")
    @mock.patch("package_admin.kernel_check")
    def test_kernel_successful(self, mock_chk, mock_output):

        """Function:  test_kernel_successful

        Description:  Test with kernel check successful.

        Arguments:

        """

        mock_output.return_value = self.status2
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
            package_admin.kernel_run(self.args, self.dnf), self.results)


if __name__ == "__main__":
    unittest.main()
