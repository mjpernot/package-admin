#!/usr/bin/python
# Classification (U)

"""Program:  get_installed_kernels.py

    Description:  Unit testing of get_installed_kernels in package_admin.py.

    Usage:
        test/unit/package_admin/get_installed_kernels.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

# Local
sys.path.append(os.getcwd())
import package_admin                            # pylint:disable=E0401,C0413
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class Package(object):                                  # pylint:disable=R0903

    """Class:  Package

    Description:  Class which is a representation of the Dnf.Package class.

    Methods:
        __init__

    """

    def __init__(self, package_list):

        """Method:  __init__

        Description:  Initialization instance of the Dnf.Package class.

        Arguments:

        """

        self.version = None
        self.pkg_name_list = list(package_list)

    def run(self):

        """Method:  __init__

        Description:  Initialization instance of the Dnf.Package class.

        Arguments:

        """

        return self.pkg_name_list


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_no_kernel
        test_two_kernel
        test_one_kernel

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        data = "python-1.1"
        data2 = "kernel-core-7.8"
        list1 = [data, data2]
        list2 = [data, data2, "kernel-core-7.7"]
        list3 = [data]
        self.pkgs1 = Package(list1)
        self.pkgs2 = Package(list2)
        self.pkgs3 = Package(list3)

        self.results1 = [data2]
        self.results2 = [data2, "kernel-core-7.7"]
        self.results3 = list()

    def test_no_kernel(self):

        """Function:  test_no_kernel

        Description:  Test with no kernels in list.

        Arguments:

        """

        self.assertEqual(
            package_admin.get_installed_kernels(self.pkgs3), self.results3)

    def test_two_kernel(self):

        """Function:  test_two_kernel

        Description:  Test with two kernels in list.

        Arguments:

        """

        self.assertEqual(
            package_admin.get_installed_kernels(self.pkgs2), self.results2)

    def test_one_kernel(self):

        """Function:  test_one_kernel

        Description:  Test one kernel in list.

        Arguments:

        """

        self.assertEqual(
            package_admin.get_installed_kernels(self.pkgs1), self.results1)


if __name__ == "__main__":
    unittest.main()
