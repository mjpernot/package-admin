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
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class ProgramLock(object):

    """Class:  ProgramLock

    Description:  Class stub holder for gen_class.ProgramLock class.

    Methods:
        __init__ -> Class initialization.

    """

    def __init__(self, cmdline, flavor):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            (input) cmdline -> Argv command line.
            (input) flavor -> Lock flavor ID.

        """

        self.cmdline = cmdline
        self.flavor = flavor


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
        test_run_program -> Test run_program function.
        test_programlock_true -> Test with ProgramLock returns True.
        test_programlock_false -> Test with ProgramLock returns False.
        test_programlock_id -> Test ProgramLock with flavor ID.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args_array = {"-c": "TEST_FILE", "-d": "TEST_DIR", "-I": True}
        self.args_array2 = {"-c": "TEST_FILE", "-d": "TEST_DIR", "-I": True,
                            "-y": "Flavor"}
        self.proglock = ProgramLock(["cmdline"], "FlavorID")

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

    @mock.patch("package_admin.run_program", mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_class.ProgramLock")
    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.arg_parser")
    def test_file_chk_false(self, mock_arg, mock_help, mock_lock):

        """Function:  test_file_chk_false

        Description:  Test arg_file_chk if returns false.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_cond_req.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_file_chk.return_value = False
        mock_lock.return_value = self.proglock

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.run_program", mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_class.ProgramLock")
    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.arg_parser")
    def test_run_program(self, mock_arg, mock_help, mock_lock):

        """Function:  test_run_program

        Description:  Test run_program function.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_cond_req.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_file_chk.return_value = False
        mock_lock.return_value = self.proglock

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.run_program", mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_class.ProgramLock")
    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.arg_parser")
    def test_programlock_true(self, mock_arg, mock_help, mock_lock):

        """Function:  test_programlock_true

        Description:  Test with ProgramLock returns True.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_cond_req.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_file_chk.return_value = False
        mock_lock.return_value = self.proglock

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.run_program", mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_class.ProgramLock")
    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.arg_parser")
    def test_programlock_false(self, mock_arg, mock_help, mock_lock):

        """Function:  test_programlock_false

        Description:  Test with ProgramLock returns False.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_cond_req.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_file_chk.return_value = False
        mock_lock.side_effect = \
            package_admin.gen_class.SingleInstanceException

        with gen_libs.no_std_out():
            self.assertFalse(package_admin.main())

    @mock.patch("package_admin.run_program", mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_class.ProgramLock")
    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.arg_parser")
    def test_programlock_id(self, mock_arg, mock_help, mock_lock):

        """Function:  test_programlock_id

        Description:  Test ProgramLock with flavor ID.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array2
        mock_help.return_value = False
        mock_arg.arg_cond_req.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_arg.arg_file_chk.return_value = False
        mock_lock.return_value = self.proglock

        self.assertFalse(package_admin.main())


if __name__ == "__main__":
    unittest.main()
