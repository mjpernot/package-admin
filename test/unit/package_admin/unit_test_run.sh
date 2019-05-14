#!/bin/bash
# Unit testing program for the package_admin.py module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit test:  package_admin.py"
test/unit/package_admin/help_message.py
test/unit/package_admin/process_yum.py
test/unit/package_admin/list_upd_pkg.py
test/unit/package_admin/list_ins_pkg.py
test/unit/package_admin/list_repo.py
test/unit/package_admin/run_program.py
test/unit/package_admin/main.py

