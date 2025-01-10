#!/bin/bash
# Blackbox testing program for the package_admin.py program.

# Setup the test files for all blackbox tests.
BASE_PATH=$PWD

echo "Scenario 1:  package_admin blackbox testing...Write installed packages on server to a file"
./package_admin.py -L -z -o test/blackbox/package_admin/tmp/package_out.txt | grep -E -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -L -n -o

echo ""
echo "Scenario 2:  package_admin blackbox testing...Write any available update packages to a file"
./package_admin.py -U -z -o test/blackbox/package_admin/tmp/package_out.txt | grep -E -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -U -n -o

echo ""
echo "Scenario 3:  package_admin blackbox testing...Write repositories to a file"
./package_admin.py -R -z -o test/blackbox/package_admin/tmp/package_out.txt | grep -E -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -R -n -o

echo ""
echo "Scenario 4:  package_admin blackbox testing...Write installed packages on server to a file in JSON format"
./package_admin.py -L -z -f -n -o test/blackbox/package_admin/tmp/package_out.txt | grep -E -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -L -j -n -o

echo ""
echo "Scenario 5:  package_admin blackbox testing...Write any available update packages to a file in JSON format"
./package_admin.py -U -f -z -n -o test/blackbox/package_admin/tmp/package_out.txt | grep -E -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -U -j -n -o

echo ""
echo "Scenario 6:  package_admin blackbox testing...Write repositories to a file in JSON format"
./package_admin.py -U -f -z -n -o test/blackbox/package_admin/tmp/package_out.txt | grep -E -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -U -j -n -o

