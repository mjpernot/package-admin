#!/bin/bash
# Unit test code coverage for package_admin.py module.
# This will run the Python code coverage module against all integration test modules.
# This will show the amount of code that was tested and which lines of code
#	that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=package_admin test/integration/package_admin/process_yum.py
coverage run -a --source=package_admin test/integration/package_admin/list_upd_pkg.py
coverage run -a --source=package_admin test/integration/package_admin/list_repo.py
coverage run -a --source=package_admin test/integration/package_admin/list_ins_pkg.py
coverage run -a --source=package_admin test/integration/package_admin/run_program.py
coverage run -a --source=package_admin test/integration/package_admin/main.py

echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
