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
import mongo_lib.mongo_libs as mongo_libs
import mongo_lib.mongo_class as mongo_class
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


def mongo_check(mongo_cfg, hostname, dbn, tbl):

    """Function:  mongo_check

    Description:  Validates the contents of the mongo database.

    Arguments:
        (input) mongo_cfg -> Mongo server configuration.
        (input) hostname -> Host name of the server running the check.
        (input) dbn -> Name of the database in Mongo.
        (input) tbl -> Name of the table in Mongo.

    """

    coll = mongo_libs.crt_coll_inst(mongo_cfg, dbn, tbl)
    coll.connect()

    status = True if coll.coll_find1()["Server"] == hostname else False

    mongo_libs.disconnect([coll])

    return status


def mongo_cleanup(mongo_cfg, dbn):

    """Function:  mongo_cleanup

    Description:  Cleans up the contents of the mongo database.

    Arguments:
        (input) mongo_cfg -> Mongo server configuration.
        (input) dbn -> Name of the database in Mongo.

    """

    mongo = mongo_class.DB(
        mongo_cfg.name, mongo_cfg.user, mongo_cfg.japd, host=mongo_cfg.host,
        port=mongo_cfg.port, db=dbn, auth=mongo_cfg.auth,
        conf_file=mongo_cfg.conf_file)

    mongo.db_connect(dbn)
    mongo.db_cmd("dropDatabase")
    mongo_libs.disconnect([mongo])


def _check_status(status, status_1, status_2):

    """Function:  _check_status

    Description:  Private function for main function.

    Arguments:
        (input) status -> Status of check.
        (input) status1 -> File check status.
        (input) status2 -> Mongo check status.
        (output) status -> True|False - Status of check.

    """

    if not (status_1 and status_2):
        status = False

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

    cmdline = gen_libs.get_inst(sys)
    base_dir = "test/blackbox/package_admin"
    test_path = os.path.join(os.getcwd(), base_dir)
    config_path = os.path.join(test_path, "config")
    tmp_path = os.path.join(test_path, "tmp")
    out_file = os.path.join(tmp_path, "package_out.txt")
    ext = datetime.datetime.strftime(datetime.datetime.now(),
                                     "%Y-%m-%d_%H:%M:%S")
    hold_file = out_file + "." + ext + ".HOLD"
    search_list = ["AsOf", "Server"]
    status = True
    mongo_cfg = gen_libs.load_module("mongo", config_path)
    hostname = socket.gethostname()
    dbn = "test_sysmon"
    tbl = "test_server_pkgs"

    if "-L" in cmdline.argv:
        search_list.append("InstalledPackages")

    elif "-U" in cmdline.argv:
        search_list.append("UpdatePackages")

    elif "-R" in cmdline.argv:
        search_list.append("Repos")

    if "-j" in cmdline.argv and "-o" in cmdline.argv and "-i" in cmdline.argv:
        status_1 = file_check(out_file, hold_file, search_list, json_fmt=True)
        status_2 = mongo_check(mongo_cfg, hostname, dbn, tbl)
        mongo_cleanup(mongo_cfg, dbn)
        status = _check_status(status, status_1, status_2)

    elif "-j" in cmdline.argv and "-o" in cmdline.argv:
        status = file_check(out_file, hold_file, search_list, json_fmt=True)

    elif "-i" in cmdline.argv and "-o" in cmdline.argv:
        status_1 = file_check(out_file, hold_file, search_list)
        status_2 = mongo_check(mongo_cfg, hostname, dbn, tbl)
        mongo_cleanup(mongo_cfg, dbn)
        status = _check_status(status, status_1, status_2)

    elif "-i" in cmdline.argv:
        status = mongo_check(mongo_cfg, hostname, dbn, tbl)
        mongo_cleanup(mongo_cfg, dbn)

    elif "-o" in cmdline.argv:
        status = file_check(out_file, hold_file, search_list)

    if status:
        print("\n\tTest Successful")

    else:
        print("\n\tTest Failure")


if __name__ == "__main__":
    sys.exit(main())
