#!/usr/bin/python
# Classification (U)

"""Program:  run_program.py

    Description:  Unit testing of run_program in package_admin.py.

    Usage:
        test/unit/package_admin/run_program.py

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
import lib.gen_libs as gen_libs                 # pylint:disable=E0401,C0413
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


def list_upd_pkg(args_array, yum, **kwargs):

    """Function:  list_upd_pkg

    Description:  This is a function stub for package_admin.list_upd_pkg.

    Arguments:
        args_array
        yum

    """

    status = (False, "Error Message")
    class_cfg = kwargs.get("class_cfg", None)

    if args_array and yum and class_cfg:
        status = (False, "Error Message")

    return status


def list_ins_pkg(args_array, yum, **kwargs):

    """Function:  list_ins_pkg

    Description:  This is a function stub for package_admin.list_ins_pkg.

    Arguments:
        args_array
        yum

    """

    status = (True, None)
    class_cfg = kwargs.get("class_cfg", None)

    if args_array and yum and class_cfg:
        status = (True, None)

    return status


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
        self.args_array = {}

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)

    def get_args_keys(self):

        """Method:  get_args_keys

        Description:  Method stub holder for gen_class.ArgParser.get_args_keys.

        Arguments:

        """

        return list(self.args_array.keys())


class Yum(object):                                      # pylint:disable=R0903

    """Class:  Yum

    Description:  Class which is a representation of the Yum class.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the Dnf class.

        Arguments:

        """

        self.hostname = ""
        self.data = ""


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_func_failed
        test_func_successful
        test_args_array_true
        test_args_array_false
        test_loop_zero
        test_loop_one

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.yum = Yum()
        self.args = ArgParser()
        self.args_array = {"-c": "mongo", "-d": "config"}
        self.args_array2 = {"-c": "mongo", "-d": "config", "-L": True}
        self.args_array3 = {"-c": "mongo", "-d": "config", "-U": True}
        self.func_dict1 = {"-L": list_ins_pkg}
        self.func_dict2 = {"-U": list_upd_pkg}

    @mock.patch("package_admin.gen_libs.load_module")
    def test_func_failed(self, mock_load):

        """Function:  test_func_failed

        Description:  Test with failed function run.

        Arguments:

        """

        self.args.args_array = self.args_array3

        mock_load.return_value = "Config_File"

        with gen_libs.no_std_out():
            self.assertFalse(
                package_admin.run_program(self.args, self.func_dict2))

    @mock.patch("package_admin.gen_libs.load_module")
    def test_func_successful(self, mock_load):

        """Function:  test_func_successful

        Description:  Test with successful function run.

        Arguments:

        """

        self.args.args_array = self.args_array2

        mock_load.return_value = "Config_File"

        self.assertFalse(package_admin.run_program(self.args, self.func_dict1))

    @mock.patch("package_admin.gen_libs.load_module")
    def test_args_array_true(self, mock_load):

        """Function:  test_args_array_true

        Description:  Test args_array if statement for true.

        Arguments:

        """

        self.args.args_array = self.args_array

        mock_load.return_value = "Config_File"

        self.assertFalse(package_admin.run_program(self.args, self.func_dict1))

    @mock.patch("package_admin.gen_libs.load_module")
    def test_args_array_false(self, mock_load):

        """Function:  test_args_array_false

        Description:  Test args_array if statement for false.

        Arguments:

        """

        self.args.args_array = self.args_array

        mock_load.return_value = "Config_File"

        self.assertFalse(package_admin.run_program(self.args, self.func_dict1))

    @mock.patch("package_admin.gen_libs.load_module")
    def test_loop_zero(self, mock_load):

        """Function:  test_loop_zero

        Description:  Test loop with zero loops.

        Arguments:

        """

        self.args.args_array = self.args_array

        mock_load.return_value = "Config_File"

        self.assertFalse(package_admin.run_program(self.args, self.func_dict1))

    @mock.patch("package_admin.gen_libs.load_module")
    def test_loop_one(self, mock_load):

        """Function:  test_loop_one

        Description:  Test loop with one loop.

        Arguments:

        """

        self.args.args_array = self.args_array2

        mock_load.return_value = "Config_File"

        self.assertFalse(package_admin.run_program(self.args, self.func_dict1))


if __name__ == "__main__":
    unittest.main()
