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
import package_admin
import version

__version__ = version.__version__


class Package(object):

    def __init__(self, version):
        self.version = version

    def evr_cmp(self, running):
        if self.version > running.version:
            return 1
        else:
            return 0


class Dnf(object):

    """Class:  Dnf

    Description:  Class which is a representation of the Dnf class.

    Methods:
        __init__

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
        test_reboot_false4
        test_reboot_false3
        test_reboot_false2
        test_reboot_false
        test_reboot_true4
        test_reboot_true3
        test_reboot_true2
        test_reboot_true
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
            self.pkg1.version, self.pkg2.version, self.pkg3.version]
        self.kernel_list2 = [self.pkg1.version]
        self.kernel_list3 = [self.pkg1.version, self.pkg2.version]

        self.status = (True, None)
        self.status2 = (
            False, "Note: kernel_check: Only one kernel version found")

        self.results = dict(self.data)
        self.results["Kernel"] = dict()
        self.results["Kernel"]["Current"] = str(self.pkg1.version)
        self.results["Kernel"]["Installed"] = self.pkg1.version

    @mock.patch("package_admin.get_latest_kernel")
    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_reboot_false4(self, mock_dict, mock_installed, mock_running,
                           mock_latest):

        """Function:  test_reboot_false4

        Description:  No reboot is required.

        Arguments:

        """

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list
        mock_running.return_value = self.pkg3
        mock_latest.return_value = self.pkg2

        status, data = package_admin.kernel_check(self.dnf)

        self.assertFalse(status, self.status)

    @mock.patch("package_admin.get_latest_kernel")
    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_reboot_false3(self, mock_dict, mock_installed, mock_running,
                           mock_latest):

        """Function:  test_reboot_false3

        Description:  No reboot is required.

        Arguments:

        """

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list
        mock_running.return_value = self.pkg3
        mock_latest.return_value = self.pkg2

        status, data = package_admin.kernel_check(self.dnf)

        self.assertFalse(data["Kernel"]["RebootRequired"])

    @mock.patch("package_admin.get_latest_kernel")
    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_reboot_false2(self, mock_dict, mock_installed, mock_running,
                           mock_latest):

        """Function:  test_reboot_false2

        Description:  No reboot is required.

        Arguments:

        """

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list3
        mock_running.return_value = self.pkg3
        mock_latest.return_value = self.pkg2

        status, data = package_admin.kernel_check(self.dnf)

        self.assertFalse(status, self.status)

    @mock.patch("package_admin.get_latest_kernel")
    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_reboot_false(self, mock_dict, mock_installed, mock_running,
                          mock_latest):

        """Function:  test_reboot_false

        Description:  No reboot is required.

        Arguments:

        """

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list3
        mock_running.return_value = self.pkg3
        mock_latest.return_value = self.pkg2

        status, data = package_admin.kernel_check(self.dnf)

        self.assertFalse(data["Kernel"]["RebootRequired"])

    @mock.patch("package_admin.get_latest_kernel")
    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_reboot_true4(self, mock_dict, mock_installed, mock_running,
                         mock_latest):

        """Function:  test_reboot_true4

        Description:  Reboot is required.

        Arguments:

        """

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list
        mock_running.return_value = self.pkg1
        mock_latest.return_value = self.pkg2

        status, data = package_admin.kernel_check(self.dnf)

        self.assertEqual(status, self.status)

    @mock.patch("package_admin.get_latest_kernel")
    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_reboot_true3(self, mock_dict, mock_installed, mock_running,
                         mock_latest):

        """Function:  test_reboot_true3

        Description:  Reboot is required.

        Arguments:

        """

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list
        mock_running.return_value = self.pkg1
        mock_latest.return_value = self.pkg2

        status, data = package_admin.kernel_check(self.dnf)

        self.assertTrue(data["Kernel"]["RebootRequired"])

    @mock.patch("package_admin.get_latest_kernel")
    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_reboot_true2(self, mock_dict, mock_installed, mock_running,
                         mock_latest):

        """Function:  test_reboot_true2

        Description:  Reboot is required.

        Arguments:

        """

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list3
        mock_running.return_value = self.pkg1
        mock_latest.return_value = self.pkg2

        status, data = package_admin.kernel_check(self.dnf)

        self.assertEqual(status, self.status)

    @mock.patch("package_admin.get_latest_kernel")
    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_reboot_true(self, mock_dict, mock_installed, mock_running,
                         mock_latest):

        """Function:  test_reboot_true

        Description:  Reboot is required.

        Arguments:

        """

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list3
        mock_running.return_value = self.pkg1
        mock_latest.return_value = self.pkg2

        status, data = package_admin.kernel_check(self.dnf)

        self.assertTrue(data["Kernel"]["RebootRequired"])

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
        mock_running.return_value = self.pkg1.version

        status, data = package_admin.kernel_check(self.dnf)

        self.assertEqual(status, self.status2)

    @mock.patch("package_admin.get_running_kernel")
    @mock.patch("package_admin.get_installed_kernels")
    @mock.patch("package_admin.create_template_dict")
    def test_one_kernel_found(self, mock_dict, mock_installed, mock_running):

        """Function:  test_one_kernel_found

        Description:  Found one kernel version in the package installed list.

        Arguments:

        """

        mock_dict.return_value = self.data2
        mock_installed.return_value = self.kernel_list2
        mock_running.return_value = self.pkg1.version

        status, data = package_admin.kernel_check(self.dnf)

        self.assertEqual(data["Kernel"], self.results["Kernel"])


if __name__ == "__main__":
    unittest.main()
