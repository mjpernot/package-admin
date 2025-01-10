#!/usr/bin/python
# Classification (U)

"""Program:  kernel_check.py

    Description:  Unit testing of kernel_check in package_admin.py.

    Usage:
        test/unit/package_admin/kernel_check.py

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


class Package(object):                                  # pylint:disable=R0903

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


class Dnf(object):                                      # pylint:disable=R0903

    """Class:  Dnf

    Description:  Class which is a representation of the Dnf class.

    Methods:
        __init__
        get_install_pkgs

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the Dnf class.

        Arguments:

        """

        self.host_name = None
        self.installed_pkgs = ['Pkg1', 'Pkg2']

    def get_install_pkgs(self):

        """Method:  get_install_pkgs

        Description:  Stud holder for Dnf.get_install_pkgs method.

        Arguments:

        """

        return self.installed_pkgs


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_dict
        test_no_dict
        test_reboot_no4
        test_reboot_no3
        test_reboot_no2
        test_reboot_no
        test_reboot_yes4
        test_reboot_yes3
        test_reboot_yes2
        test_reboot_yes
        test_one_kernel_found2
        test_one_kernel_found

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.dnf = Dnf()
        self.data = {
            "Server": "Server_Name", "OsRelease": "OS_Release",
            "AsOf": "2024-02-14 14:15:45"}
        self.data2 = dict()
        self.pkg1 = Package(1)
        self.pkg2 = Package(2)
        self.pkg3 = Package(3)
        self.kernel_list = [
            self.pkg1.kversion, self.pkg2.kversion, self.pkg3.kversion]
        self.kernel_list2 = [self.pkg1.kversion]
        self.kernel_list3 = [self.pkg1.kversion, self.pkg2.kversion]

        self.status = (True, None)

        self.results = dict(self.data)
        self.results["Kernel"] = dict()
        self.results["Kernel"]["Current"] = str(self.pkg1.kversion)
        self.results["Kernel"]["Installed"] = self.pkg1.kversion

    @mock.patch("package_admin.get_latest_kernel")
    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    def test_dict(self, mock_installed, mock_running, mock_latest):

        """Function:  test_dict

        Description:  Test with dictionary passed.

        Arguments:

        """

        mock_installed.return_value = self.kernel_list
        mock_running.return_value = self.pkg1
        mock_latest.return_value = self.pkg2

        status, _ = package_admin.kernel_check(self.dnf, self.data)

        self.assertEqual(status, self.status)

    @mock.patch("package_admin.get_latest_kernel")
    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_no_dict(self, mock_dict, mock_installed, mock_running,
                     mock_latest):

        """Function:  test_no_dict

        Description:  Test with no dictionary passed.

        Arguments:

        """

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list
        mock_running.return_value = self.pkg1
        mock_latest.return_value = self.pkg2

        status, _ = package_admin.kernel_check(self.dnf)

        self.assertEqual(status, self.status)

    @mock.patch("package_admin.get_latest_kernel")
    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_reboot_no4(self, mock_dict, mock_installed, mock_running,
                        mock_latest):

        """Function:  test_reboot_no4

        Description:  No reboot is required.

        Arguments:

        """

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list
        mock_running.return_value = self.pkg3
        mock_latest.return_value = self.pkg2

        status, _ = package_admin.kernel_check(self.dnf)

        self.assertEqual(status, self.status)

    @mock.patch("package_admin.get_latest_kernel")
    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_reboot_no3(self, mock_dict, mock_installed, mock_running,
                        mock_latest):

        """Function:  test_reboot_no3

        Description:  No reboot is required.

        Arguments:

        """

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list
        mock_running.return_value = self.pkg3
        mock_latest.return_value = self.pkg2

        _, data = package_admin.kernel_check(self.dnf)

        self.assertEqual(data["Kernel"]["RebootRequired"], "No")

    @mock.patch("package_admin.get_latest_kernel")
    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_reboot_no2(self, mock_dict, mock_installed, mock_running,
                        mock_latest):

        """Function:  test_reboot_no2

        Description:  No reboot is required.

        Arguments:

        """

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list3
        mock_running.return_value = self.pkg3
        mock_latest.return_value = self.pkg2

        status, _ = package_admin.kernel_check(self.dnf)

        self.assertEqual(status, self.status)

    @mock.patch("package_admin.get_latest_kernel")
    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_reboot_no(self, mock_dict, mock_installed, mock_running,
                       mock_latest):

        """Function:  test_reboot_no

        Description:  No reboot is required.

        Arguments:

        """

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list3
        mock_running.return_value = self.pkg3
        mock_latest.return_value = self.pkg2

        _, data = package_admin.kernel_check(self.dnf)

        self.assertEqual(data["Kernel"]["RebootRequired"], "No")

    @mock.patch("package_admin.get_latest_kernel")
    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_reboot_yes4(self, mock_dict, mock_installed, mock_running,
                         mock_latest):

        """Function:  test_reboot_yes4

        Description:  Reboot is required.

        Arguments:

        """

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list
        mock_running.return_value = self.pkg1
        mock_latest.return_value = self.pkg2

        status, _ = package_admin.kernel_check(self.dnf)

        self.assertEqual(status, self.status)

    @mock.patch("package_admin.get_latest_kernel")
    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_reboot_yes3(self, mock_dict, mock_installed, mock_running,
                         mock_latest):

        """Function:  test_reboot_yes3

        Description:  Reboot is required.

        Arguments:

        """

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list
        mock_running.return_value = self.pkg1
        mock_latest.return_value = self.pkg2

        _, data = package_admin.kernel_check(self.dnf)

        self.assertEqual(data["Kernel"]["RebootRequired"], "Yes")

    @mock.patch("package_admin.get_latest_kernel")
    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_reboot_yes2(self, mock_dict, mock_installed, mock_running,
                         mock_latest):

        """Function:  test_reboot_yes2

        Description:  Reboot is required.

        Arguments:

        """

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list3
        mock_running.return_value = self.pkg1
        mock_latest.return_value = self.pkg2

        status, _ = package_admin.kernel_check(self.dnf)

        self.assertEqual(status, self.status)

    @mock.patch("package_admin.get_latest_kernel")
    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_reboot_yes(self, mock_dict, mock_installed, mock_running,
                        mock_latest):

        """Function:  test_reboot_yes

        Description:  Reboot is required.

        Arguments:

        """

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list3
        mock_running.return_value = self.pkg1
        mock_latest.return_value = self.pkg2

        _, data = package_admin.kernel_check(self.dnf)

        self.assertEqual(data["Kernel"]["RebootRequired"], "Yes")

    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_one_kernel_found2(self, mock_dict, mock_installed, mock_running):

        """Function:  test_one_kernel_found2

        Description:  Found one kernel version in the package installed list.

        Arguments:

        """

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list2
        mock_running.return_value = self.pkg1.kversion

        status, _ = package_admin.kernel_check(self.dnf)

        self.assertEqual(status, self.status)

    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_one_kernel_found(self, mock_dict, mock_installed, mock_running):

        """Function:  test_one_kernel_found

        Description:  Found one kernel version in the package installed list.

        Arguments:

        """

        self.results["Kernel"]["RebootRequired"] = "No"

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list2
        mock_running.return_value = self.pkg1.kversion

        _, data = package_admin.kernel_check(self.dnf)

        self.assertEqual(data["Kernel"], self.results["Kernel"])


if __name__ == "__main__":
    unittest.main()
