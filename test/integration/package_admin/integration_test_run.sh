#!/bin/bash
# Integration testing program for the package_admin.py program.
# This will run all the integrations tests for this program.
# Will need to run this from the base directory where the program file
#   is located at.

echo ""
echo "Integration test:  process_yum"
test/integration/package_admin/process_yum.py

echo ""
echo "Integration test:  list_upd_pkg"
test/integration/package_admin/list_upd_pkg.py

echo ""
echo "Integration test:  list_ins_pkg"
test/integration/package_admin/list_ins_pkg.py

echo ""
echo "Integration test:  list_repo"
test/integration/package_admin/list_repo.py

echo ""
echo "Integration test:  run_program"
test/integration/package_admin/run_program.py

echo ""
echo "Integration test:  main"
test/integration/package_admin/main.py

