#!/usr/bin/python
# Classification (U)

"""Program:  main.py

    Description:  Unit testing of main in package_admin.py.

    Usage:
        test/unit/package_admin/main.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import package_admin
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Unit testing initilization.
        test_help_true -> Test help if returns true.
        test_help_false -> Test help if returns false.
        test_cond_req_false -> Test arg_cond_req if returns false.
        test_cond_req_true -> Test arg_cond_req if returns true.
        test_dir_chk_true -> Test arg_dir_chk_crt if returns true.
        test_dir_chk_false -> Test arg_dir_chk_crt if returns false.
        test_file_chk_true -> Test arg_file_chk if returns true.
        test_file_chk_false -> Test arg_file_chk if returns false.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args_array = {"-c": "TEST_FILE", "-d": "TEST_DIR", "-I": True}

    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.arg_parser.arg_parse2")
    def test_help_true(self, mock_arg, mock_help):

        """Function:  test_help_true

        Description:  Test help if returns true.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = True

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.arg_parser.arg_cond_req")
    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.arg_parser.arg_parse2")
    def test_help_false(self, mock_arg, mock_help, mock_cond):

        """Function:  test_help_false

        Description:  Test help if returns false.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = False
        mock_cond.return_value = False

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.arg_parser.arg_cond_req")
    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.arg_parser.arg_parse2")
    def test_cond_req_false(self, mock_arg, mock_help, mock_cond):

        """Function:  test_cond_req_false

        Description:  Test arg_cond_req if returns false.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = False
        mock_cond.return_value = False

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.arg_parser.arg_dir_chk_crt")
    @mock.patch("package_admin.arg_parser.arg_cond_req")
    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.arg_parser.arg_parse2")
    def test_cond_req_true(self, mock_arg, mock_help, mock_cond, mock_dir_chk):

        """Function:  test_cond_req_true

        Description:  Test arg_cond_req if returns true.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = False
        mock_cond.return_value = True
        mock_dir_chk.return_value = True

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.arg_parser.arg_dir_chk_crt")
    @mock.patch("package_admin.arg_parser.arg_cond_req")
    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.arg_parser.arg_parse2")
    def test_dir_chk_true(self, mock_arg, mock_help, mock_cond, mock_dir_chk):

        """Function:  test_dir_chk_true

        Description:  Test arg_dir_chk_crt if returns true.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = False
        mock_cond.return_value = True
        mock_dir_chk.return_value = True

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.arg_parser.arg_file_chk")
    @mock.patch("package_admin.arg_parser.arg_dir_chk_crt")
    @mock.patch("package_admin.arg_parser.arg_cond_req")
    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.arg_parser.arg_parse2")
    def test_dir_chk_false(self, mock_arg, mock_help, mock_cond, mock_dir_chk,
                           mock_file_chk):

        """Function:  test_dir_chk_false

        Description:  Test arg_dir_chk_crt if returns false.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = False
        mock_cond.return_value = True
        mock_dir_chk.return_value = False
        mock_file_chk.return_value = True

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.arg_parser.arg_file_chk")
    @mock.patch("package_admin.arg_parser.arg_dir_chk_crt")
    @mock.patch("package_admin.arg_parser.arg_cond_req")
    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.arg_parser.arg_parse2")
    def test_file_chk_true(self, mock_arg, mock_help, mock_cond, mock_dir_chk,
                           mock_file_chk):

        """Function:  test_file_chk_true

        Description:  Test arg_file_chk if returns true.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = False
        mock_cond.return_value = True
        mock_dir_chk.return_value = False
        mock_file_chk.return_value = True

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.run_program")
    @mock.patch("package_admin.arg_parser.arg_file_chk")
    @mock.patch("package_admin.arg_parser.arg_dir_chk_crt")
    @mock.patch("package_admin.arg_parser.arg_cond_req")
    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.arg_parser.arg_parse2")
    def test_file_chk_false(self, mock_arg, mock_help, mock_cond, mock_dir_chk,
                            mock_file_chk, mock_run):

        """Function:  test_file_chk_false

        Description:  Test arg_file_chk if returns false.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = False
        mock_cond.return_value = True
        mock_dir_chk.return_value = False
        mock_file_chk.return_value = False
        mock_run.return_value = True

        self.assertFalse(package_admin.main())


if __name__ == "__main__":
    unittest.main()
