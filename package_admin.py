#!/usr/bin/python
# Classification (U)

"""Program:      package_admin.py

    Description:  Linux Package administration program for handling packages on
        a Linux server using yum.  This program has a number of functions to
        include listing current packages, listing any new package updates,
        installing package updates, and listing current repositories.

    Usage:
        package_admin.py
            {-L [-f] [-z] [-e to_email [to_email2 ...] [-s subject_line] [-u]]
                [-o dir_path/file [-a]] |
             -R [-f] [-z] [-e to_email [to_email2 ...] [-s subject_line] [-u]]
                 [-o dir_path/file [-a]] |
             -U [-f] [-z] [-i db_name:table_name -c file -d path]
                 [-e to_email [to_email2 ...] [-s subject_line] [-u]]
                 [-o dir_path/file [-a]]}
            [-y flavor_id] [-v | -h]

    Arguments:
        -L => List all packages installed on the server.
            -f => Flatten the JSON data structure.
            -z => Suppress standard out.
            -e to_email_address(es) => Sends output to one or more email
                    addresses.  Email addresses are space delimited.
                -s subject_line => Subject line of email.Will create own
                    subject line if one is not provided.
                -u => Override the default mail command and use mailx.
            -o path/file => Directory path and file name for output.
                -a => Append output to output file.

        -U => List update packages awaiting for the server.
            -f => Flatten the JSON data structure.
            -z => Suppress standard out.
            -i { database:collection } => Name of database and collection to
                    insert into Mongo database.  Default:  sysmon:server_pkgs
                -c file => Mongo server configuration file.
                -d dir path => Directory path to config file (-c).
            -e to_email_address(es) => Sends output to one or more email
                    addresses.  Email addresses are space delimited.
                -s subject_line => Subject line of email.Will create own
                    subject line if one is not provided.
                -u => Override the default mail command and use mailx.
            -o path/file => Directory path and file name for output.
                -a => Append output to output file.

        -R => List current repositories.
            -f => Flatten the JSON data structure.
            -z => Suppress standard out.
            -e to_email_address(es) => Sends output to one or more email
                    addresses.  Email addresses are space delimited.
                -s subject_line => Subject line of email.Will create own
                    subject line if one is not provided.
                -u => Override the default mail command and use mailx.
            -o path/file => Directory path and file name for output.
                -a => Append output to output file.

        -y value => A flavor id for the program lock.  To create unique lock.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1: -v and -h overrides all other options.

    Notes:
        Mongo configuration file format (config/mongo.py.TEMPLATE).
        The configuration file format for the Mongo connection used for
        inserting data into a database.

        There are two ways to connect methods:  single Mongo database or a
        Mongo replica set.

            Single Configuration file for Mongo Database Server.
            user = "USER"
            japd = "PSWORD"
            host = "HOST_IP"
            name = "HOSTNAME"
            port = 27017
            conf_file = None
            auth = True
            auth_db = "admin"
            auth_mech = "SCRAM-SHA-1"
            use_arg = True
            use_uri = False

            Replica set connection:  Same format as above, but with these
                additional entries at the end of the configuration file.  By
                default all these entries are set to None to represent not
                connecting to a replica set.

            repset = "REPLICA_SET_NAME"
            repset_hosts = "HOST1:PORT, HOST2:PORT, [...]"
            db_auth = "AUTHENTICATION_DATABASE"

            Note:  If using SSL connections then set one or more of the
                following entries.  This will automatically enable SSL
                connections. Below are the configuration settings for SSL
                connections.  See configuration file for details on each entry:

            ssl_client_ca = None
            ssl_client_key = None
            ssl_client_cert = None
            ssl_client_phrase = None

            FIPS Environment for Mongo:  If operating in a FIPS 104-2
                environment, this package will require at least a minimum of
                pymongo==3.8.0 or better.  It will also require a manual change
                to the auth.py module in the pymongo package.  See below for
                changes to auth.py.  In addition, other modules may require to
                have the same modification as the auth.py module.  If a
                stacktrace occurs and it states "= hashlib.md5()" is the
                problem, then note the module name "= hashlib.md5()" is in and
                make the same change as in auth.py:  "usedforsecurity=False".
            - Locate the auth.py file python installed packages on the system
                in the pymongo package directory.
            - Edit the file and locate the "_password_digest" function.
            - In the "_password_digest" function there is an line that should
                match: "md5hash = hashlib.md5()".  Change it to
                "md5hash = hashlib.md5(usedforsecurity=False)".
            - Lastly, it will require the Mongo configuration file entry
                auth_mech to be set to: SCRAM-SHA-1 or SCRAM-SHA-256.

        Configuration modules -> Name is runtime dependent as it can be used to
            connect to different databases with different names.

    Example:
        package_admin.py -U -f -c mongo -d config -i

"""

# Libraries and Global Variables

# Standard
import sys
import datetime

# Third-Party
import json

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import mongo_lib.mongo_libs as mongo_libs
import version

__version__ = version.__version__


def help_message():

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def process_yum(args_array, yum, dict_key, func_name, **kwargs):

    """Function:  process_yum

    Description:  Create and populate dictionary form based on the dict_key and
        func_name.  Send dictionary to output.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (input) yum -> Yum class instance.
        (input) dict_key -> Dictionary key value.
        (input) func_name -> Name of class method to call.
        (input) **kwargs:
            class_cfg -> Mongo server configuration.
        (output) status -> Tuple on connection status.
            status[0] - True|False - Mongo connection successful.
            status[1] - Error message if Mongo connection failed.

    """

    status = (True, None)
    args_array = dict(args_array)
    os_distro = yum.get_distro()
    data = {"Server": yum.get_hostname(),
            "OsRelease": os_distro[0] + " " + os_distro[1],
            "AsOf": datetime.datetime.strftime(datetime.datetime.now(),
                                               "%Y-%m-%d %H:%M:%S"),
            dict_key: func_name()}
    ofile = args_array.get("-o", False)
    db_tbl = args_array.get("-i", False)
    class_cfg = kwargs.get("class_cfg", False)
    mode = "a" if args_array.get("-a", False) else "w"
    indent = None if args_array.get("-f", False) else 4

    if db_tbl and class_cfg:
        dbn, tbl = db_tbl.split(":")
        status = mongo_libs.ins_doc(class_cfg, dbn, tbl, data)

        if not status[0]:
            status = (status[0], "Mongo_Insert: " + status[1])

    data = json.dumps(data, indent=indent)

    if ofile:
        gen_libs.write_file(ofile, mode, data)

    if not args_array.get("-z", False):
        gen_libs.display_data(data)

    if args_array.get("-e", False):
        mail = gen_class.setup_mail(
            args_array.get("-e"), subj=args_array.get("-s", None))
        mail.add_2_msg(data)
        use_mailx = args_array.get("-u", False)
        mail.send_mail(use_mailx=use_mailx)

    return status


def list_upd_pkg(args_array, yum, **kwargs):

    """Function:  list_upd_pkg

    Description:  List any packages available for updates on the server.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (input) yum -> Yum class instance.
        (input) **kwargs:
            class_cfg -> Mongo server configuration.
        (output) status -> Tuple on connection status.
            status[0] - True|False - Mongo connection successful.
            status[1] - Error message if Mongo connection failed.

    """

    args_array = dict(args_array)
    status = process_yum(
        args_array, yum, "UpdatePackages", yum.fetch_update_pkgs, **kwargs)

    if not status[0]:
        status = (status[0], "list_upd_pkg: " + status[1])

    return status


def list_ins_pkg(args_array, yum, **kwargs):

    """Function:  list_ins_pkg

    Description:  List all currently installed packages on the server.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (input) yum -> Yum class instance.
        (input) **kwargs:
            class_cfg -> Mongo server configuration.
        (output) status -> Tuple on connection status.
            status[0] - True|False - Mongo connection successful.
            status[1] - Error message if Mongo connection failed.

    """

    args_array = dict(args_array)
    status = process_yum(
        args_array, yum, "InstalledPackages", yum.fetch_install_pkgs, **kwargs)

    if not status[0]:
        status = (status[0], "list_ins_pkg: " + status[1])

    return status


def list_repo(args_array, yum, **kwargs):

    """Function:  list_repo

    Description:  List the current list of repositories.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (input) yum -> Yum class instance.
        (input) **kwargs:
            class_cfg -> Mongo server configuration.
        (output) status -> Tuple on connection status.
            status[0] - True|False - Mongo connection successful.
            status[1] - Error message if Mongo connection failed.

    """

    args_array = dict(args_array)
    status = process_yum(args_array, yum, "Repos", yum.fetch_repos, **kwargs)

    if not status[0]:
        status = (status[0], "list_repo: " + status[1])

    return status


def run_program(args_array, func_dict):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.

    Arguments:
        (input) args_array -> Dict of command line options and values.
        (input) func_dict -> Dictionary list of functions and options.

    """

    args_array = dict(args_array)
    func_dict = dict(func_dict)
    yum = gen_class.Yum()
    mongo_cfg = None

    if args_array.get("-c", False):
        mongo_cfg = gen_libs.load_module(args_array["-c"], args_array["-d"])

    # Intersect args_array & func_dict to find which functions to call.
    for item in set(args_array.keys()) & set(func_dict.keys()):
        status = func_dict[item](args_array, yum, class_cfg=mongo_cfg)

        if not status[0]:
            print("Error Detected: %s" % (status[1]))


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_chk_list -> contains options which will be directories.
        file_chk_list -> contains the options which will have files included.
        file_crt_list -> contains options which require files to be created.
        func_dict -> dictionary list for the function calls or other options.
        opt_def_dict -> contains options with their default values.
        opt_con_req_list -> contains the options that require other options.
        opt_multi_list -> contains the options that will have multiple values.
        opt_val_list -> contains options which require values.

    Arguments:
        (input) argv -> Arguments from the command line.

    """

    cmdline = gen_libs.get_inst(sys)
    dir_chk_list = ["-d"]
    file_chk_list = ["-o"]
    file_crt_list = ["-o"]
    func_dict = {"-L": list_ins_pkg, "-U": list_upd_pkg, "-R": list_repo}
    opt_def_dict = {"-i": "sysmon:server_pkgs"}
    opt_con_req_list = {"-i": ["-c", "-d"], "-s": ["-e"], "-u": ["-e"]}
    opt_multi_list = ["-e", "-s"]
    opt_val_list = ["-c", "-d", "-i", "-o", "-e", "-s", "-y"]

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(
        cmdline.argv, opt_val_list, opt_def_dict, multi_val=opt_multi_list)

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and arg_parser.arg_cond_req(args_array, opt_con_req_list) \
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list) \
       and not arg_parser.arg_file_chk(args_array, file_chk_list,
                                       file_crt_list):

        try:
            proglock = gen_class.ProgramLock(
                cmdline.argv, args_array.get("-y", ""))
            run_program(args_array, func_dict)
            del proglock

        except gen_class.SingleInstanceException:
            print("WARNING:  Lock in place for package_admin with id of: %s"
                  % (args_array.get("-y", "")))


if __name__ == "__main__":
    sys.exit(main())
