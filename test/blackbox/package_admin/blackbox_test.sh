#!/bin/bash
# Blackbox testing program for the package_admin.py program.

# Setup the test files for all blackbox tests.
BASE_PATH=$PWD

echo "Scenario 1:  package_admin blackbox testing...Write installed packages on server to a file"
./package_admin.py -L -z -o test/blackbox/package_admin/tmp/package_out.txt | egrep -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -L -n -o

echo ""
echo "Scenario 2:  package_admin blackbox testing...Write any available update packages to a file"
./package_admin.py -U -z -o test/blackbox/package_admin/tmp/package_out.txt | egrep -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -U -n -o

echo ""
echo "Scenario 3:  package_admin blackbox testing...Write repositories to a file"
./package_admin.py -R -z -o test/blackbox/package_admin/tmp/package_out.txt | egrep -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -R -n -o

echo ""
echo "Scenario 4:  package_admin blackbox testing...Write installed packages on server to a file in JSON format"
./package_admin.py -L -f -n -o test/blackbox/package_admin/tmp/package_out.txt | egrep -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -L -j -n -o

echo ""
echo "Scenario 5:  package_admin blackbox testing...Write any available update packages to a file in JSON format"
./package_admin.py -U -f -n -o test/blackbox/package_admin/tmp/package_out.txt | egrep -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -U -j -n -o

echo ""
echo "Scenario 6:  package_admin blackbox testing...Write repositories to a file in JSON format"
./package_admin.py -U -f -n -o test/blackbox/package_admin/tmp/package_out.txt | egrep -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -U -j -n -o

echo ""
echo "Scenario 7:  package_admin blackbox testing...Write installed packages on server to mongodb"
./package_admin.py -L -z -i test_sysmon:test_server_pkgs -c mongo -d $PWD/test/blackbox/package_admin/config | egrep -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -L -n -i

echo ""
echo "Scenario 8:  package_admin blackbox testing...Write any available update packages to mongodb"
./package_admin.py -U -z -i test_sysmon:test_server_pkgs -c mongo -d $PWD/test/blackbox/package_admin/config | egrep -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -U -n -i

echo ""
echo "Scenario 9:  package_admin blackbox testing...Write repositories to mongodb"
./package_admin.py -R -z -i test_sysmon:test_server_pkgs -c mongo -d $PWD/test/blackbox/package_admin/config | egrep -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -R -n -i

echo ""
echo "Scenario 10:  package_admin blackbox testing...Write installed packages on server to mongodb and a file"
./package_admin.py -L -z -i test_sysmon:test_server_pkgs -c mongo -d $PWD/test/blackbox/package_admin/config -o test/blackbox/package_admin/tmp/package_out.txt | egrep -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -L -n -i -o

echo ""
echo "Scenario 11:  package_admin blackbox testing...Write any available update packages to mongodb and a file"
./package_admin.py -U -z -i test_sysmon:test_server_pkgs -c mongo -d $PWD/test/blackbox/package_admin/config -o test/blackbox/package_admin/tmp/package_out.txt | egrep -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -U -n -i -o

echo ""
echo "Scenario 12:  package_admin blackbox testing...Write repositories to mongodb and a file"
./package_admin.py -R -z -i test_sysmon:test_server_pkgs -c mongo -d $PWD/test/blackbox/package_admin/config -o test/blackbox/package_admin/tmp/package_out.txt | egrep -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -R -n -i -o

echo ""
echo "Scenario 13:  package_admin blackbox testing...Write installed packages on server to mongodb and a file in JSON format"
./package_admin.py -L -z -f -i test_sysmon:test_server_pkgs -c mongo -d $PWD/test/blackbox/package_admin/config -o test/blackbox/package_admin/tmp/package_out.txt | egrep -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -L -n -i -o -j

echo ""
echo "Scenario 14:  package_admin blackbox testing...Write any available update packages to mongodb and a file in JSON format"
./package_admin.py -U -z -f -i test_sysmon:test_server_pkgs -c mongo -d $PWD/test/blackbox/package_admin/config -o test/blackbox/package_admin/tmp/package_out.txt | egrep -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -U -n -i -o -j

echo ""
echo "Scenario 15:  package_admin blackbox testing...Write repositories to mongodb and a file in JSON format"
./package_admin.py -R -z -f -i test_sysmon:test_server_pkgs -c mongo -d $PWD/test/blackbox/package_admin/config -o test/blackbox/package_admin/tmp/package_out.txt | egrep -v "Loaded plugins: fastestmirror|Loading mirror speeds from cached hostfile"
test/blackbox/package_admin/blackbox_test.py -R -n -i -o -j

