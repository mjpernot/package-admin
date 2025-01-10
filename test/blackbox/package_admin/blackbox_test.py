#!/usr/bin/python
# Classification (U)

"""Program:  blackbox_test.py

    Description:  Blackbox testing of package_admin.py program.

    Usage:
        test/blackbox/package_admin/blackbox_test.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import os
import sys
import datetime
import shutil
import socket

# Third-party
import json

# Local
sys.path.append(os.getcwd())
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


def file_check(out_file, hold_file, search_list, json_fmt=False):

    """Function:  file_check

    Description:  Check the contents of the output file based on the items in
        the search_list variable and check to see if file is in JSON format.

    Arguments:
        (input) out_file -> Path and file name of output file.
        (input) hold_file -> Name of file if file check fail.
        (input) search_list -> List of items to be checked for in output file.
        (input) json_fmt -> True|False -> Output file is in JSON format.
        (output) status -> True|False - Status of checks.

    """

    status = True

    if os.path.isfile(out_file):
        for item in search_list:
            if item not in open(out_file).read():
                status = False
                print("\t\tError:  %s not present in %s" % (item, out_file))

                if not os.path.isfile(hold_file):
                    shutil.copy2(out_file, hold_file)

        if json_fmt:
            status = _check_json(out_file, status, hold_file)

        os.remove(out_file)

    else:
        status = False
        print("\t\tError:  %s is not present" % (out_file))

    return status


def _check_json(out_file, status, hold_file):

    """Function:  _check_json

    Description:  Private function for file_check function.

    Arguments:
        (input) out_file -> Path and file name of output file.
        (input) status -> Status of check.
        (input) hold_file -> Name of file if file check fail.
        (output) status -> True|False - Status of check.

    """

    try:
        _ = json.load(open(out_file))

    except ValueError:
        status = False
        print("\t\tError:  %s is not in JSON format" % (out_file))

        if not os.path.isfile(hold_file):
            shutil.copy2(out_file, hold_file)

    return status


def main():

    """Function:  main

    Description:  Control the blackbox testing of package_admin.py program.

    Variables:
        base_dir -> Directory path to blackbox testing directory.
        tmp_path -> Current base_dir plus tmp directory.
        out_file -> Path and file name of output file.
        ext -> Extension to be added to output file that contains errors.
        hold_file -> Name of file if file checks fail.
        search_list -> List of items to be checked for in output file.
        status -> True|False - Status of checks.

    Arguments:

    """

    base_dir = "test/blackbox/package_admin"
    test_path = os.path.join(os.getcwd(), base_dir)
    tmp_path = os.path.join(test_path, "tmp")
    out_file = os.path.join(tmp_path, "package_out.txt")
    ext = datetime.datetime.strftime(datetime.datetime.now(),
                                     "%Y-%m-%d_%H:%M:%S")
    hold_file = out_file + "." + ext + ".HOLD"
    search_list = ["AsOf", "Server"]
    status = True
    hostname = socket.gethostname()
    dbn = "test_sysmon"
    tbl = "test_server_pkgs"

    if "-L" in sys.argv:
        search_list.append("InstalledPackages")

    elif "-U" in sys.argv:
        search_list.append("UpdatePackages")

    elif "-R" in sys.argv:
        search_list.append("Repos")

    if "-j" in sys.argv and "-o" in sys.argv:
        status = file_check(out_file, hold_file, search_list, json_fmt=True)

    elif "-o" in sys.argv:
        status = file_check(out_file, hold_file, search_list)

    if status:
        print("\n\tTest Successful")

    else:
        print("\n\tTest Failure")


if __name__ == "__main__":
    sys.exit(main())
