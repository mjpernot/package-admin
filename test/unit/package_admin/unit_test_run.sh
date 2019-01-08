#!/bin/bash
# Unit testing program for the package_admin.py module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit test:  help_message"
test/unit/package_admin/help_message.py

echo ""
echo "Unit test:  process_yum"
test/unit/package_admin/process_yum.py

echo ""
echo "Unit test:  list_upd_pkg"
test/unit/package_admin/list_upd_pkg.py

echo ""
echo "Unit test:  list_ins_pkg"
test/unit/package_admin/list_ins_pkg.py

echo ""
echo "Unit test:  list_repo"
test/unit/package_admin/list_repo.py

echo ""
echo "Unit test:  run_program"
test/unit/package_admin/run_program.py

echo ""
echo "Unit test:  main"
test/unit/package_admin/main.py

