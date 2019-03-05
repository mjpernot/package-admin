#!/usr/bin/python
# Classification (U)

"""Program:      package_admin.py

    Description:  Linux Package administration program for handling packages on
        a Linux server.  This program has a number of functions to include
        listing current packages, listing any new package updates, installing
        package updates, and listing current repositories.

    Usage:
        package_admin.py { -L | -U | -R } { -j }
            { -i db_name:table_name -c file -d path } { -v | -h }

    Arguments:
        -L => List all packages installed on the server.
        -U => List update packages awaiting for the server.
        -R => List current repositories.
        -j => Return output in JSON format.
        -i { database:collection } => Name of database and collection to
            insert the database statistics data into.  Available for -U option.
            Requires options:  -c and -d
            Default:  sysmon:server_pkgs
        -c file => Mongo server configuration file.  Required for -i option.
        -d dir path => Directory path to config file (-c).  Required for -i
            option.
        -n => No standard out.  Do not send output to standard out.
        -o path/file => Directory path and file name for output.
            Available for -L, -U, and -R options.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1: -v and -h overrides all other options.

    Notes:
        Mongo configuration file format (mongo.py).  The configuration file
        format for the Mongo connection used for inserting data into a
        database.  There are two ways to connect:  single or replica set.

            1.)  Mongo single database connection:

            # All Mongo configuration settings.
            user = "USER"
            passwd = "PASSWORD"
            # Mongo DB host information
            host = "IP_ADDRESS"
            name = "HOSTNAME"
            # Mongo database port (default is 27017)
            port = 27017
            # Mongo configuration settings
            conf_file = None
            # Authentication required:  True|False
            auth = True

            2.)  Mongo replica set connection:
            Same format as single Mongo database connection and with these
            additional entries in the configuration file:

            # Replica Set Mongo configuration settings.
            # Replica set name.
            #    None means the Mongo database is not part of a replica set.
            #    Example:  repset = "REPLICA_SET_NAME"
            repset = None
            # Replica host listing.
            #    None means the Mongo database is not part of a replica set.
            #    Example:  repset_hosts = "HOST1:PORT, HOST2:PORT, [...]"
            repset_hosts = None
            # Database to authentication to.
            #    Example:  db_auth = "AUTHENTICATION_DATABASE"
            db_auth = None

        Configuration modules -> Name is runtime dependent as it can be used to
            connect to different databases with different names.

    Example:
        package_admin.py -U -j -c mongo -d config -i

"""

# Libraries and Global Variables

# Standard
import sys
import datetime

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import mongo_lib.mongo_libs as mongo_libs
import version

# Version
__version__ = version.__version__


def help_message(**kwargs):

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:
        (input) **kwargs:
            None

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

    """

    os_distro = yum.get_distro()

    data = {"Server": yum.get_hostname(),
            "OS_Release": os_distro[0] + " " + os_distro[1],
            "Asof": datetime.datetime.strftime(datetime.datetime.now(),
                                               "%Y-%m-%d %H:%M:%S"),
            dict_key: func_name()}

    # Send data to output.
    if args_array.get("-i", False) and kwargs.get("class_cfg", False):

        db, tbl = args_array.get("-i").split(":")
        mongo_libs.ins_doc(kwargs.get("class_cfg"), db, tbl, data)

    err_flag, err_msg = gen_libs.data_multi_out(data,
                                                args_array.get("-o", False),
                                                args_array.get("-j", False),
                                                args_array.get("-n", False))

    if err_flag:
        print(err_msg)


def list_upd_pkg(args_array, yum, **kwargs):

    """Function:  list_upd_pkg

    Description:  List any packages available for updates on the server.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (input) yum -> Yum class instance.
        (input) **kwargs:
            class_cfg -> Mongo server configuration.

    """

    process_yum(args_array, yum, "Update_Packages", yum.fetch_update_pkgs,
                **kwargs)


def list_ins_pkg(args_array, yum, **kwargs):

    """Function:  list_ins_pkg

    Description:  List all currently installed packages on the server.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (input) yum -> Yum class instance.
        (input) **kwargs:
            class_cfg -> Mongo server configuration.

    """

    process_yum(args_array, yum, "Installed_Packages", yum.fetch_install_pkgs,
                **kwargs)


def list_repo(args_array, yum, **kwargs):

    """Function:  list_repo

    Description:  List the current list of repositories.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (input) yum -> Yum class instance.
        (input) **kwargs:
            class_cfg -> Mongo server configuration.

    """

    process_yum(args_array, yum, "Repos", yum.fetch_repos, **kwargs)


def run_program(args_array, func_dict, **kwargs):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.

    Arguments:
        (input) args_array -> Dict of command line options and values.
        (input) func_dict -> Dictionary list of functions and options.
        (input) **kwargs:
            None

    """

    yum = gen_class.Yum()
    mongo_cfg = None

    if args_array.get("-c", False):
        mongo_cfg = gen_libs.load_module(args_array["-c"], args_array["-d"])

    # Intersect args_array & func_dict to find which functions to call.
    for x in set(args_array.keys()) & set(func_dict.keys()):
        func_dict[x](args_array, yum, class_cfg=mongo_cfg, **kwargs)


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
        opt_val_list -> contains options which require values.

    Arguments:
        (input) argv -> Arguments from the command line.

    """

    dir_chk_list = ["-d"]
    file_chk_list = ["-o"]
    file_crt_list = ["-o"]
    func_dict = {"-L": list_ins_pkg, "-U": list_upd_pkg, "-R": list_repo}
    opt_def_dict = {"-i": "sysmon:server_pkgs"}
    opt_con_req_list = {"-i": ["-c", "-d"]}
    opt_val_list = ["-c", "-d", "-i", "-o"]

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(sys.argv, opt_val_list, opt_def_dict)

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and arg_parser.arg_cond_req(args_array, opt_con_req_list) \
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list) \
       and not arg_parser.arg_file_chk(args_array, file_chk_list,
                                       file_crt_list):

        run_program(args_array, func_dict)


if __name__ == "__main__":
    sys.exit(main())
