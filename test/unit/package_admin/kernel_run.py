#!/usr/bin/python
# Classification (U)

"""Program:  kernel_run.py

    Description:  Unit testing of kernel_run in package_admin.py.

    Usage:
        test/unit/package_admin/kernel_run.py

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


class ArgParser():                                      # pylint:disable=R0903

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


class Dnf():                                            # pylint:disable=R0903

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
        test_output_failure
        test_output_successful
        test_kernel_failure
        test_kernel_successful

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
        self.status3 = (False, "Output_Message")

        self.results = (False, "Kernel_Message")
        self.results2 = (True, None)
        self.results3 = (False, "Output_Message")

    @mock.patch("package_admin.output_run")
    @mock.patch("package_admin.kernel_check")
    def test_output_failure(self, mock_chk, mock_output):

        """Function:  test_output_failure

        Description:  Test with output_run failure.

        Arguments:

        """

        mock_output.return_value = self.status3
        mock_chk.return_value = self.status2, self.data

        self.assertEqual(
            package_admin.kernel_run(self.args, self.dnf), self.results3)

    @mock.patch("package_admin.output_run")
    @mock.patch("package_admin.kernel_check")
    def test_output_successful(self, mock_chk, mock_output):

        """Function:  test_output_successful

        Description:  Test with output_run successful.

        Arguments:

        """

        mock_output.return_value = self.status2
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


if __name__ == "__main__":
    unittest.main()
