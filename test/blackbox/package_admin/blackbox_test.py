#!/usr/bin/python
# Classification (U)

"""Program:  blackbox_test.py

    Description:  Blackbox testing of package_admin.py program.

    Usage:
        test/blackbox/package_admin/blackbox_test.py

    Arguments:
        None

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
import lib.cmds_gen as cmds_gen
import mongo_lib.mongo_class as mongo_class
import version

__version__ = version.__version__


def file_check(out_file, hold_file, search_list, json_fmt=False, **kwargs):

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


def _check_json(out_file, status, hold_file, **kwargs):

    """Function:  _check_json

    Description:  Private function for file_check function.

    Arguments:
        (input) out_file -> Path and file name of output file.
        (input) status -> Status of check.
        (input) hold_file -> Name of file if file check fail.
        (output) status -> True|False - Status of checks.

    """

    try:
        data = json.load(open(out_file))

    except:
        status = False
        print("\t\tError:  %s is not in JSON format" % (out_file))

        if not os.path.isfile(hold_file):
            shutil.copy2(out_file, hold_file)

    return status


def mongo_check(mongo_cfg, hostname, db, tbl, **kwargs):

    """Function:  mongo_check

    Description:  Validates the contents of the mongo database.

    Arguments:
        (input) mongo_cfg -> Mongo server configuration.
        (input) hostname -> Host name of the server running the check.
        (input) db -> Name of the database in Mongo.
        (input) tbl -> Name of the table in Mongo.

    """

    COLL = mongo_libs.crt_coll_inst(mongo_cfg, db, tbl)
    COLL.connect()

    if COLL.coll_find1()["Server"] == hostname:
        status = True

    else:
        status = False

    cmds_gen.Disconnect([COLL])

    return status


def mongo_cleanup(mongo_cfg, db, **kwargs):

    """Function:  mongo_cleanup

    Description:  Cleans up the contents of the mongo database.

    Arguments:
        (input) mongo_cfg -> Mongo server configuration.
        (input) db -> Name of the database in Mongo.

    """

    DB = mongo_class.DB(mongo_cfg.name, mongo_cfg.user, mongo_cfg.passwd,
                        mongo_cfg.host, mongo_cfg.port, db, mongo_cfg.auth,
                        mongo_cfg.conf_file)

    DB.db_connect(db)
    DB.db_cmd("dropDatabase")
    cmds_gen.Disconnect([DB])


def main():

    """Function:  main

    Description:  Control the blackbox testing of package_admin.py program.

    Variables:
        base_dir -> Directory path to blackbox testing directory.
        out_path -> Current base_dir plus out directory.
        out_file -> Path and file name of output file.
        ext -> Extension to be added to output file that contains errors.
        hold_file -> Name of file if file checks fail.
        search_list -> List of items to be checked for in output file.
        status -> True|False - Status of checks.

    Arguments:
        None

    """

    base_dir = "test/blackbox/package_admin"
    test_path = os.path.join(os.getcwd(), base_dir)
    config_path = os.path.join(test_path, "config")

    out_path = os.path.join(base_dir, "out")
    out_file = os.path.join(out_path, "package_out.txt")
    ext = datetime.datetime.strftime(datetime.datetime.now(),
                                     "%Y-%m-%d_%H:%M:%S")
    hold_file = out_file + "." + ext + ".HOLD"
    search_list = ["Asof", "Server"]
    status = True

    mongo_cfg = gen_libs.Load_Module("mongo", config_path)
    hostname = socket.gethostname()
    db = "test_sysmon"
    tbl = "test_server_pkgs"

    if "-L" in sys.argv:
        search_list.append("Installed_Packages")

    elif "-U" in sys.argv:
        search_list.append("Update_Packages")

    elif "-R" in sys.argv:
        search_list.append("Repos")

    if "-j" in sys.argv and "-o" in sys.argv and "-i" in sys.argv:
        status_1 = file_check(out_file, hold_file, search_list, json_fmt=True)
        status_2 = mongo_check(mongo_cfg, hostname, db, tbl)
        mongo_cleanup(mongo_cfg, db)

        if not (status_1 and status_2):
            status = False

    elif "-j" in sys.argv and "-o" in sys.argv:
        status = file_check(out_file, hold_file, search_list, json_fmt=True)

    elif "-i" in sys.argv and "-o" in sys.argv:
        status_1 = file_check(out_file, hold_file, search_list)
        status_2 = mongo_check(mongo_cfg, hostname, db, tbl)
        mongo_cleanup(mongo_cfg, db)

        if not (status_1 and status_2):
            status = False

    elif "-i" in sys.argv:
        status = mongo_check(mongo_cfg, hostname, db, tbl)
        mongo_cleanup(mongo_cfg, db)

    elif "-o" in sys.argv:
        status = file_check(out_file, hold_file, search_list)

    if status:
        print("\n\tTest Successful")

    else:
        print("\n\tTest Failure")


if __name__ == "__main__":
    sys.exit(main())
