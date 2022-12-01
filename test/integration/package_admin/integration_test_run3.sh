#!/bin/bash
# Integration testing program for the package_admin.py program.
# This will run all the integrations tests for this program.
# Will need to run this from the base directory where the program file
#   is located at.

echo ""
echo "Integration test:  package_admin.py"
/usr/bin/python3 test/integration/package_admin/process_yum.py
/usr/bin/python3 test/integration/package_admin/list_upd_pkg.py
/usr/bin/python3 test/integration/package_admin/list_ins_pkg.py
/usr/bin/python3 test/integration/package_admin/list_repo.py
/usr/bin/python3 test/integration/package_admin/run_program.py
/usr/bin/python3 test/integration/package_admin/main.py
