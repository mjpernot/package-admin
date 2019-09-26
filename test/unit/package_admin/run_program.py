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


def list_ins_pkg(args_array, yum, **kwargs):

    """Function:  list_ins_pkg

    Description:  This is a function stub for package_admin.list_ins_pkg.

    Arguments:
        args_array -> Stub argument holder.
        yum -> Stub argument holder.

    """

    pass


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Unit testing initilization.
        test_args_array_true -> Test args_array if statement for true.
        test_args_array_false -> Test args_array if statement for false.
        test_loop_zero -> Test loop with zero loops.
        test_loop_one -> Test loop with one loop.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class Yum(object):

            """Class:  Yum

            Description:  Class which is a representation of the Yum class.

            Methods:
                __init__ -> Initialize configuration environment.
                fetch_repos -> Set self.data attribute.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the Mail class.

                Arguments:

                """

                self.hostname = ""
                self.data = ""

        self.yum = Yum()

        self.args_array = {"-c": "mongo", "-d": "config"}
        self.func_dict = {"-L": list_ins_pkg}

    @mock.patch("package_admin.gen_libs.load_module")
    @mock.patch("package_admin.gen_class.Yum")
    def test_args_array_true(self, mock_yum, mock_load):

        """Function:  test_args_array_true

        Description:  Test args_array if statement for true.

        Arguments:

        """

        mock_yum.return_value = self.yum
        mock_load.return_value = "Config_File"

        self.assertFalse(package_admin.run_program(self.args_array,
                                                   self.func_dict))

    @mock.patch("package_admin.gen_libs.load_module")
    @mock.patch("package_admin.gen_class.Yum")
    def test_args_array_false(self, mock_yum, mock_load):

        """Function:  test_args_array_false

        Description:  Test args_array if statement for false.

        Arguments:

        """

        mock_yum.return_value = self.yum
        mock_load.return_value = "Config_File"

        self.assertFalse(package_admin.run_program(self.args_array,
                                                   self.func_dict))

    @mock.patch("package_admin.gen_libs.load_module")
    @mock.patch("package_admin.gen_class.Yum")
    def test_loop_zero(self, mock_yum, mock_load):

        """Function:  test_loop_zero

        Description:  Test loop with zero loops.

        Arguments:

        """

        mock_yum.return_value = self.yum
        mock_load.return_value = "Config_File"

        self.assertFalse(package_admin.run_program(self.args_array,
                                                   self.func_dict))

    @mock.patch("package_admin.gen_libs.load_module")
    @mock.patch("package_admin.gen_class.Yum")
    def test_loop_one(self, mock_yum, mock_load):

        """Function:  test_loop_one

        Description:  Test loop with one loop.

        Arguments:

        """

        self.args_array["-L"] = True

        mock_yum.return_value = self.yum
        mock_yum.list_ins_pkg.return_Value = True
        mock_load.return_value = "Config_File"

        self.assertFalse(package_admin.run_program(self.args_array,
                                                   self.func_dict))


if __name__ == "__main__":
    unittest.main()
