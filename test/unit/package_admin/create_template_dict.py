#!/usr/bin/python
# Classification (U)

"""Program:  create_template_dict.py

    Description:  Unit testing of create_template_dict in package_admin.py.

    Usage:
        test/unit/package_admin/create_template_dict.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import datetime
import unittest

# Local
sys.path.append(os.getcwd())
import package_admin                            # pylint:disable=E0401,C0413
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class Dnf(object):

    """Class:  Dnf

    Description:  Class which is a representation of the Dnf class.

    Methods:
        __init__
        get_distro
        get_hostname

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the Dnf class.

        Arguments:

        """

        self.os_distro = ("Linux", "7.8")
        self.server_name = "SERVER_NAME"

    def get_distro(self):

        """Method:  get_distro

        Description:  Stud holder for Dnf.get_distro method.

        Arguments:

        """

        return self.os_distro

    def get_hostname(self):

        """Method:  get_hostname

        Description:  Stud holder for Dnf.get_hostname method.

        Arguments:

        """

        return self.server_name


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_template_dict2
        test_template_dict

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.dnf = Dnf()
        self.results = {
            "Server": "SERVER_NAME", "OsRelease": "Linux 7.8",
            "AsOf": datetime.datetime.strftime(
                datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")}

    def test_template_dict2(self):

        """Function:  test_template_dict2

        Description:  Test with template dictionary.

        Arguments:

        """

        self.assertEqual(
            package_admin.create_template_dict(self.dnf)["OsRelease"],
            self.results["OsRelease"])

    def test_template_dict(self):

        """Function:  test_template_dict

        Description:  Test with template dictionary.

        Arguments:

        """

        self.assertEqual(
            package_admin.create_template_dict(self.dnf)["Server"],
            self.results["Server"])


if __name__ == "__main__":
    unittest.main()
