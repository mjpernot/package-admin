#!/usr/bin/python
# Classification (U)

"""Program:  get_latest_kernel.py

    Description:  Unit testing of get_latest_kernel in package_admin.py.

    Usage:
        test/unit/package_admin/get_latest_kernel.py

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


class Package():                                        # pylint:disable=R0903

    """Class:  Package

    Description:  Class which is a representation of the Dnf.Package class.

    Methods:
        __init__
        evr_cmp

    """

    def __init__(self, kversion):

        """Method:  __init__

        Description:  Initialization instance of the Dnf.Package class.

        Arguments:

        """

        self.kversion = kversion

    def evr_cmp(self, running):

        """Method:  evr_cmp

        Description:  Stud holder for Dnf.Package.evr_cmp method.

        Arguments:

        """

        if self.kversion > running.kversion:
            return 1

        return 0


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

        self.pkg1 = Package(1)
        self.pkg2 = Package(2)
        self.pkg3 = Package(3)
        self.kernel_list = [self.pkg1, self.pkg2, self.pkg3]
        self.kernel_list2 = [self.pkg1]
        self.kernel_list3 = [self.pkg1, self.pkg2]

    def test_three_pkgs(self):

        """Function:  test_three_pkgs

        Description:  Test with three packages in list.

        Arguments:

        """

        self.assertEqual(
            package_admin.get_latest_kernel(self.kernel_list), self.pkg3)

    def test_two_pkgs(self):

        """Function:  test_two_pkgs

        Description:  Test with two packages in list.

        Arguments:

        """

        self.assertEqual(
            package_admin.get_latest_kernel(self.kernel_list3), self.pkg2)

    def test_one_pkg(self):

        """Function:  test_one_pkg

        Description:  Test one package in list.

        Arguments:

        """

        self.assertEqual(
            package_admin.get_latest_kernel(self.kernel_list2), self.pkg1)


if __name__ == "__main__":
    unittest.main()
