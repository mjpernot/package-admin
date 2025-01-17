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
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import package_admin                        # pylint:disable=E0401,C0413
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import version                              # pylint:disable=E0401,C0413

__version__ = version.__version__


class ArgParser():

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        arg_cond_req_or
        arg_dir_chk
        arg_file_chk
        get_val
        arg_parse2

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = {}
        self.dir_perms_chk = None
        self.dir_perms_chk2 = True
        self.file_perm_chk = None
        self.file_perm_chk2 = True
        self.file_crt = None
        self.opt_con_or = None
        self.opt_con_or2 = True
        self.argparse2 = True

    def arg_cond_req_or(self, opt_con_or):

        """Method:  arg_cond_req_or

        Description:  Method stub holder for
            gen_class.ArgParser.arg_cond_req_or.

        Arguments:

        """

        self.opt_con_or = opt_con_or

        return self.opt_con_or2

    def arg_dir_chk(self, dir_perms_chk):

        """Method:  arg_dir_chk

        Description:  Method stub holder for gen_class.ArgParser.arg_dir_chk.

        Arguments:

        """

        self.dir_perms_chk = dir_perms_chk

        return self.dir_perms_chk2

    def arg_file_chk(self, file_perm_chk, file_crt):

        """Method:  arg_file_chk

        Description:  Method stub holder for gen_class.ArgParser.arg_file_chk.

        Arguments:

        """

        self.file_perm_chk = file_perm_chk
        self.file_crt = file_crt

        return self.file_perm_chk2

    def get_val(self, skey, def_val):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)

    def arg_parse2(self):

        """Method:  arg_parse2

        Description:  Method stub holder for gen_class.ArgParser.arg_parse2.

        Arguments:

        """

        return self.argparse2


class ProgramLock():                                    # pylint:disable=R0903

    """Class:  ProgramLock

    Description:  Class stub holder for gen_class.ProgramLock class.

    Methods:
        __init__

    """

    def __init__(self, cmdline, flavor):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            (input) cmdline
            (input) flavor

        """

        self.cmdline = cmdline
        self.flavor = flavor


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_arg_parse2_false
        test_arg_parse2_true
        test_help_false
        test_help_true
        test_help_true
        test_help_false
        test_cond_req_false
        test_cond_req_true
        test_dir_chk_false
        test_dir_chk_true
        test_file_chk_false
        test_file_chk_true
        test_run_program
        test_programlock_true
        test_programlock_false
        test_programlock_id

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.args_array = {"-c": "TEST_FILE", "-d": "TEST_DIR", "-I": True}
        self.args_array2 = {"-c": "TEST_FILE", "-d": "TEST_DIR", "-I": True,
                            "-y": "Flavor"}
        self.proglock = ProgramLock(["cmdline"], "FlavorID")

    @mock.patch("package_admin.gen_class.ArgParser")
    def test_arg_parse2_false(self, mock_arg):

        """Function:  test_arg_parse2_false

        Description:  Test arg_parser2 returns false.

        Arguments:

        """

        self.args.argparse2 = False

        mock_arg.return_value = self.args

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.gen_class.ArgParser")
    def test_arg_parse2_true(self, mock_arg, mock_help):

        """Function:  test_arg_parse2_true

        Description:  Test arg_parser2 returns true.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = True

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.gen_class.ArgParser")
    def test_help_true(self, mock_arg, mock_help):

        """Function:  test_help_true

        Description:  Test help if returns true.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = True

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.gen_class.ArgParser")
    def test_help_false(self, mock_arg, mock_help):

        """Function:  test_help_false

        Description:  Test help if returns false.

        Arguments:

        """

        self.args.opt_con_or2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.gen_class.ArgParser")
    def test_cond_req_false(self, mock_arg, mock_help):

        """Function:  test_cond_req_false

        Description:  Test arg_cond_req if returns false.

        Arguments:

        """

        self.args.opt_con_or2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.gen_class.ArgParser")
    def test_cond_req_true(self, mock_arg, mock_help):

        """Function:  test_cond_req_true

        Description:  Test arg_cond_req if returns true.

        Arguments:

        """

        self.args.dir_perms_chk2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.gen_class.ArgParser")
    def test_dir_chk_false(self, mock_arg, mock_help):

        """Function:  test_dir_chk_false

        Description:  Test arg_dir_chk_crt if returns false.

        Arguments:

        """

        self.args.dir_perms_chk2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.gen_class.ArgParser")
    def test_dir_chk_true(self, mock_arg, mock_help):

        """Function:  test_dir_chk_true

        Description:  Test arg_dir_chk_crt if returns true.

        Arguments:

        """

        self.args.file_perm_chk2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.gen_class.ArgParser")
    def test_file_chk_false(self, mock_arg, mock_help):

        """Function:  test_file_chk_false

        Description:  Test arg_file_chk_crt if returns false.

        Arguments:

        """

        self.args.file_perm_chk2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.run_program", mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_class.ProgramLock")
    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.gen_class.ArgParser")
    def test_file_chk_true(self, mock_arg, mock_help, mock_lock):

        """Function:  test_file_chk_true

        Description:  Test arg_file_chk if returns true.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = False
        mock_lock.return_value = self.proglock

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.run_program", mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_class.ProgramLock")
    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.gen_class.ArgParser")
    def test_run_program(self, mock_arg, mock_help, mock_lock):

        """Function:  test_run_program

        Description:  Test run_program function.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = False
        mock_lock.return_value = self.proglock

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.run_program", mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_class.ProgramLock")
    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.gen_class.ArgParser")
    def test_programlock_true(self, mock_arg, mock_help, mock_lock):

        """Function:  test_programlock_true

        Description:  Test with ProgramLock returns True.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = False
        mock_lock.return_value = self.proglock

        self.assertFalse(package_admin.main())

    @mock.patch("package_admin.run_program", mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_class.ProgramLock")
    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.gen_class.ArgParser")
    def test_programlock_false(self, mock_arg, mock_help, mock_lock):

        """Function:  test_programlock_false

        Description:  Test with ProgramLock returns False.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = False
        mock_lock.side_effect = \
            package_admin.gen_class.SingleInstanceException

        with gen_libs.no_std_out():
            self.assertFalse(package_admin.main())

    @mock.patch("package_admin.run_program", mock.Mock(return_value=True))
    @mock.patch("package_admin.gen_class.ProgramLock")
    @mock.patch("package_admin.gen_libs.help_func")
    @mock.patch("package_admin.gen_class.ArgParser")
    def test_programlock_id(self, mock_arg, mock_help, mock_lock):

        """Function:  test_programlock_id

        Description:  Test ProgramLock with flavor ID.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = False
        mock_lock.return_value = self.proglock

        self.assertFalse(package_admin.main())


if __name__ == "__main__":
    unittest.main()
