#!/bin/bash
# Unit test code coverage for SonarQube to cover all modules.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#	that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=package_admin test/unit/package_admin/create_template_dict.py
coverage run -a --source=package_admin test/unit/package_admin/display_data.py
coverage run -a --source=package_admin test/unit/package_admin/help_message.py
coverage run -a --source=package_admin test/unit/package_admin/get_installed_kernels.py
coverage run -a --source=package_admin test/unit/package_admin/get_latest_kernel.py
coverage run -a --source=package_admin test/unit/package_admin/get_running_kernel.py
coverage run -a --source=package_admin test/unit/package_admin/kernel_check.py
coverage run -a --source=package_admin test/unit/package_admin/list_ins_pkg.py
coverage run -a --source=package_admin test/unit/package_admin/list_upd_pkg.py
coverage run -a --source=package_admin test/unit/package_admin/list_repo.py
coverage run -a --source=package_admin test/unit/package_admin/mail_data.py
coverage run -a --source=package_admin test/unit/package_admin/main.py
coverage run -a --source=package_admin test/unit/package_admin/mongo_insert.py
coverage run -a --source=package_admin test/unit/package_admin/output_run.py
coverage run -a --source=package_admin test/unit/package_admin/process_yum.py
coverage run -a --source=package_admin test/unit/package_admin/rabbitmq_publish.py
coverage run -a --source=package_admin test/unit/package_admin/run_program.py
coverage run -a --source=package_admin test/unit/package_admin/write_file.py

echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
coverage xml -i

