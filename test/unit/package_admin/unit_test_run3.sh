#!/bin/bash
# Unit testing program for the package_admin.py module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit test:  package_admin.py"
/usr/bin/python3 ./test/unit/package_admin/create_template_dict.py
/usr/bin/python3 ./test/unit/package_admin/help_message.py
/usr/bin/python3 ./test/unit/package_admin/get_installed_kernels.py
/usr/bin/python3 ./test/unit/package_admin/get_latest_kernel.py
/usr/bin/python3 ./test/unit/package_admin/get_running_kernel.py
/usr/bin/python3 ./test/unit/package_admin/kernel_check.py
/usr/bin/python3 ./test/unit/package_admin/kernel_run3.py
/usr/bin/python3 ./test/unit/package_admin/process_yum.py
/usr/bin/python3 ./test/unit/package_admin/list_upd_pkg.py
/usr/bin/python3 ./test/unit/package_admin/list_ins_pkg.py
/usr/bin/python3 ./test/unit/package_admin/list_repo.py
/usr/bin/python3 ./test/unit/package_admin/run_program.py
/usr/bin/python3 ./test/unit/package_admin/main.py

