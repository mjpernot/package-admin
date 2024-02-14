#!/usr/bin/python
# Classification (U)

"""Program:  get_running_kernel.py

    Description:  Unit testing of get_running_kernel in package_admin.py.

    Usage:
        test/unit/package_admin/get_running_kernel.py

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


class Package(object):

    """Class:  Package

    Description:  Class which is a representation of the Dnf.Package class.

    Methods:
        __init__
        evr

    """

    def __init__(self, version):

        """Method:  __init__

        Description:  Initialization instance of the Dnf.Package class.

        Arguments:

        """

        self.version = version
        self.evr = version

    def evr(self):

        """Method:  evr

        Description:  Stud holder for Dnf.Package.evr_cmp method.

        Arguments:

        """

        return self.version


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_three_pkgs
        test_two_pkgs
        test_one_pkg

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.pkg1 = Package("1")
        self.pkg2 = Package("2")
        self.pkg3 = Package("3")
        self.kernel_list = [self.pkg1, self.pkg2, self.pkg3]
        self.kernel_list2 = [self.pkg1]
        self.kernel_list3 = [self.pkg1, self.pkg2]

    @mock.patch("package_admin.platform.release", mock.Mock(return_value="2"))
    def test_three_pkgs(self):

        """Function:  test_three_pkgs

        Description:  Test with three packages in list.

        Arguments:

        """

        self.assertEqual(
            package_admin.get_running_kernel(self.kernel_list), self.pkg2)

    @mock.patch("package_admin.platform.release", mock.Mock(return_value="2"))
    def test_two_pkgs(self):

        """Function:  test_two_pkgs

        Description:  Test with two packages in list.

        Arguments:

        """

        self.assertEqual(
            package_admin.get_running_kernel(self.kernel_list3), self.pkg2)

    @mock.patch("package_admin.platform.release", mock.Mock(return_value="1"))
    def test_one_pkg(self):

        """Function:  test_one_pkg

        Description:  Test one package in list.

        Arguments:

        """

        self.assertEqual(
            package_admin.get_running_kernel(self.kernel_list2), self.pkg1)


if __name__ == "__main__":
    unittest.main()
