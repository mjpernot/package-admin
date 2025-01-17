#!/usr/bin/python
# Classification (U)

"""Program:      package_admin.py

    Description:  Linux Package administration program for handling packages on
        a Linux server using dnf.  This program has a number of functions to
        include listing current packages, listing any new package updates,
        installing package updates, and listing current repositories.

    Usage:
        package_admin.py
            {-L [-f] [-z] [-e to_email [to_email2 ...] [-s subject_line] [-u]]
                [-o dir_path/file [-a]] [-r -b file -d path] |
             -R [-f] [-z] [-e to_email [to_email2 ...] [-s subject_line] [-u]]
                 [-o dir_path/file [-a]] [-r -b file -d path] |
             -U [-f] [-z]
                 [-e to_email [to_email2 ...] [-s subject_line] [-u]]
                 [-o dir_path/file [-a]] [-r -b file -d path] |
             -K [-f] [-z]
                 [-e to_email [to_email2 ...] [-s subject_line] [-u]]
                 [-o dir_path/file [-a]] [-r -b file -d path]}
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
            -r => Publish entry to RabbitMQ.
                -b file => RabbitMQ configuration file.
                -d dir path => Directory path to config file (-b).

        -U => List update packages awaiting for the server.
            -f => Flatten the JSON data structure.
            -z => Suppress standard out.
            -k => Include a kernel check with this option.
            -e to_email_address(es) => Sends output to one or more email
                    addresses.  Email addresses are space delimited.
                -s subject_line => Subject line of email.Will create own
                    subject line if one is not provided.
                -u => Override the default mail command and use mailx.
            -o path/file => Directory path and file name for output.
                -a => Append output to output file.
            -r => Publish entry to RabbitMQ.
                -b file => RabbitMQ configuration file.
                -d dir path => Directory path to config file (-b).

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
            -r => Publish entry to RabbitMQ.
                -b file => RabbitMQ configuration file.
                -d dir path => Directory path to config file (-b).

        -K => Kernel check to see current and installed versions match.
            -f => Flatten the JSON data structure.
            -z => Suppress standard out.
            -e to_email_address(es) => Sends output to one or more email
                    addresses.  Email addresses are space delimited.
                -s subject_line => Subject line of email.Will create own
                    subject line if one is not provided.
                -u => Override the default mail command and use mailx.
            -o path/file => Directory path and file name for output.
                -a => Append output to output file.
            -r => Publish entry to RabbitMQ.
                -b file => RabbitMQ configuration file.
                -d dir path => Directory path to config file (-b).

        -y value => A flavor id for the program lock.  To create unique lock.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1: -v and -h overrides all other options.

    Notes:
        RabbitMQ configuration file format (config/rabbitmq.py.TEMPLATE).
        The configuration file format is for connecting and publishing to a
        RabbitMQ.

            # Login information.
            user = "USER"
            japd = "PSWORD"
            host = "HOSTNAME"
            host_list = []
            queue = "QUEUENAME"
            r_key = "RKEYNAME"
            exchange_name = "EXCHANGE_NAME"
            port = 5672
            exchange_type = "direct"
            x_durable = True
            q_durable = True
            auto_delete = False

        Configuration modules -> Name is runtime dependent as it can be used to
            connect to different databases with different names.

    Example:
        package_admin.py -U -f -b rabbitmq -d config -r

"""

# Libraries and Global Variables

# Standard
import sys
import datetime
import platform

try:
    import simplejson as json
except ImportError:
    import json

# Local
try:
    from .lib import gen_libs
    from .lib import gen_class
    from .lib import gen_dnf
    from .rabbit_lib import rabbitmq_class
    from . import version

except (ValueError, ImportError) as err:
    import lib.gen_libs as gen_libs                     # pylint:disable=R0402
    import lib.gen_class as gen_class                   # pylint:disable=R0402
    import lib.gen_dnf as gen_dnf                       # pylint:disable=R0402
    import rabbit_lib.rabbitmq_class as rabbitmq_class  # pylint:disable=R0402
    import version

__version__ = version.__version__


def help_message():

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def process_yum(args, dnf, dict_key, func_name):

    """Function:  process_yum

    Description:  Create and populate dictionary form based on the dict_key and
        func_name.  Send dictionary to output.

    Arguments:
        (input) args -> ArgParser class instance
        (input) dnf -> Dnf class instance
        (input) dict_key -> Dictionary key value
        (input) func_name -> Name of class method to call
        (output) status -> Tuple on connection status
            status[0] - True|False - RabbitMQ connection successful
            status[1] - Error message if RabbitMQ connection failed

    """

    status = (True, None)
    os_distro = dnf.get_distro()
    data = {"Server": dnf.get_hostname(),
            "OsRelease": os_distro[0] + " " + os_distro[1],
            "AsOf": datetime.datetime.strftime(
                datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"),
            dict_key: func_name()}
    ofile = args.get_val("-o", def_val=False)
    mode = "a" if args.get_val("-a", def_val=False) else "w"
    indent = None if args.get_val("-f", def_val=False) else 4

    if args.get_val("-r", def_val=False):
        cfg = gen_libs.load_module(args.get_val("-b"), args.get_val("-d"))
        t_status = rabbitmq_class.pub_2_rmq(cfg, json.dumps(data))

        if not t_status[0]:
            status = (t_status[0], "RabbitMQ: " + t_status[1])

    data = json.dumps(data, indent=indent)

    if ofile:
        gen_libs.write_file(ofile, mode, data)

    if not args.get_val("-z", def_val=False):
        gen_libs.display_data(data)

    if args.get_val("-e", def_val=False):
        mail = gen_class.setup_mail(
            args.get_val("-e"), subj=args.get_val("-s", def_val=None))
        mail.add_2_msg(data)
        use_mailx = args.get_val("-u", def_val=False)
        mail.send_mail(use_mailx=use_mailx)

    return status


def list_upd_pkg(args, dnf, **kwargs):

    """Function:  list_upd_pkg

    Description:  List any packages available for updates on the server.

    Arguments:
        (input) args -> ArgParser class instance
        (input) dnf -> Dnf class instance
        (input) **kwargs:
            data -> Dictionary containing server details
        (output) status -> Tuple on connection status
            status[0] - True|False - kernel check successful
            status[1] - Error message if kernel check failed

    """

    data = dict(kwargs.get("data")) \
        if kwargs.get("data", None) else create_template_dict(dnf)
    data["UpdatePackages"] = dnf.fetch_update_pkgs()

    if args.get_val("-k", def_val=False) and sys.version_info >= (3, 0):
        status, data = kernel_check(dnf, data)

        if status[0]:
            status = output_run(args, data)
    else:
        status = output_run(args, data)

    return status


def list_ins_pkg(args, dnf):

    """Function:  list_ins_pkg

    Description:  List all currently installed packages on the server.

    Arguments:
        (input) args -> ArgParser class instance
        (input) dnf -> Dnf class instance
        (output) status -> Tuple on connection status
            status[0] - True|False - RabbitMQ connection successful
            status[1] - Error message if RabbitMQ connection failed

    """

    status = process_yum(
        args, dnf, "InstalledPackages", dnf.fetch_install_pkgs)

    if not status[0]:
        status = (status[0], "list_ins_pkg: " + status[1])

    return status


def list_repo(args, dnf):

    """Function:  list_repo

    Description:  List the current list of repositories.

    Arguments:
        (input) args -> ArgParser class instance
        (input) dnf -> Dnf class instance
        (output) status -> Tuple on connection status
            status[0] - True|False - RabbitMQ connection successful
            status[1] - Error message if RabbitMQ connection failed

    """

    status = process_yum(args, dnf, "Repos", dnf.fetch_repos)

    if not status[0]:
        status = (status[0], "list_repo: " + status[1])

    return status


def create_template_dict(dnf):

    """Function:  create_template_dict

    Description:  Set up dictionary with server-level details.

    Arguments:
        (input) dnf -> Dnf class instance
        (output) data -> Dictionary containing server details

    """

    os_distro = dnf.get_distro()
    data = {"Server": dnf.get_hostname(),
            "OsRelease": os_distro[0] + " " + os_distro[1],
            "AsOf": datetime.datetime.strftime(
                datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")}

    return data


def get_installed_kernels(pkgs_installed):

    """Function:  get_installed_kernels

    Description:  Return the installed kernel versions on the server.

    Arguments:
        (input) pkgs_installed -> Dnf.get_install_pkgs class instance
        (output) kernel_list -> List of installed kernel version instances

    """

    kernel_name = "kernel-core"
    kernel_list = []

    for pkg in pkgs_installed.run():

        if kernel_name in str(pkg):
            kernel_list.append(pkg)

    return kernel_list


def get_running_kernel(kernel_list):

    """Function:  get_running_kernel

    Description:  Return the running kernel version.

    Arguments:
        (input) kernel_list -> List of kernel version instances
        (output) running -> Current running kernel instance

    """

    for pkg in kernel_list:

        if pkg.evr in platform.release():
            running = pkg
            break

    return running


def get_latest_kernel(kernel_list):

    """Function:  get_latest_kernel

    Description:  Return the latest kernel version.

    Arguments:
        (input) kernel_list -> List of kernel version instances
        (output) latest -> Latest kernel version instance

    """

    latest = kernel_list[0]

    for pkg in kernel_list:

        if pkg.evr_cmp(latest) == 1:
            latest = pkg

    return latest


def kernel_check(dnf, data=None):

    """Function:  kernel_check

    Description:  Compares the current running kernel version to the latest
        installed kernel version and determines if a reboot is required.

    Note:  This is only available for the Dnf class use.

    Arguments:
        (input) dnf -> Dnf class instance
        (input) data -> Dictionary from package listing
        (output) status -> Tuple on operation status
            status[0] - True|False - successful operation
            status[1] - Error message
        (output) data -> Dictionary that has the kernel version status

    """

    status = (True, None)
    pkgs_installed = dnf.get_install_pkgs()
    data = dict(data) if data else create_template_dict(dnf)
    data["Kernel"] = {}
    kernel_list = get_installed_kernels(pkgs_installed)
    running = get_running_kernel(kernel_list)
    data["Kernel"]["Current"] = str(running)

    if len(kernel_list) > 1:
        latest = get_latest_kernel(kernel_list)
        data["Kernel"]["Installed"] = str(latest)

        if latest.evr_cmp(running) == 1:
            data["Kernel"]["RebootRequired"] = "Yes"

        elif latest.evr_cmp(running) == 0:
            data["Kernel"]["RebootRequired"] = "No"

        else:
            status = (
                False,
                "Error: kernel_check: Couldn't determine if reboot required")

    elif len(kernel_list) == 1:
        data["Kernel"]["Installed"] = kernel_list[0]
        data["Kernel"]["RebootRequired"] = "No"

    else:
        status = (False, "Error: kernel_check: No kernel versions found")

    return status, data


def rabbitmq_publish(args, data):

    """Function:  rabbitmq_publish

    Description:  Publish data to RabbitMQ.

    Arguments:
        (input) args -> ArgParser class instance
        (input) data -> Dictionary that has package data
        (output) status -> Tuple on RabbitMQ publication status
            status[0] - True|False - Successful operation
            status[1] - Error message

    """

    status = (True, None)
    data = dict(data)

    if args.get_val("-r", def_val=False):
        cfg = gen_libs.load_module(args.get_val("-b"), args.get_val("-d"))
        status = rabbitmq_class.pub_2_rmq(cfg, json.dumps(data))

    return status


def write_file(args, data):

    """Function:  write_file

    Description:  Write data to a file.

    Arguments:
        (input) args -> ArgParser class instance
        (input) data -> Dictionary that has package data

    """

    ofile = args.get_val("-o", def_val=False)
    mode = "a" if args.get_val("-a", def_val=False) else "w"

    if ofile:
        gen_libs.write_file(ofile, mode, data)


def display_data(args, data):

    """Function:  display_data

    Description:  Display data to terminal.

    Arguments:
        (input) args -> ArgParser class instance
        (input) data -> String dictionary that has package data

    """

    if not args.get_val("-z", def_val=False):
        gen_libs.display_data(data)


def mail_data(args, data):

    """Function:  mail_data

    Description:  Email data out.

    Arguments:
        (input) args -> ArgParser class instance
        (input) data -> String dictionary that has package data

    """

    if args.get_val("-e", def_val=False):
        mail = gen_class.setup_mail(
            args.get_val("-e"), subj=args.get_val("-s", def_val=None))
        mail.add_2_msg(data)
        use_mailx = args.get_val("-u", def_val=False)
        mail.send_mail(use_mailx=use_mailx)


def output_run(args, data):

    """Function:  output_run

    Description:  Directs where the data output will go.

    Arguments:
        (input) args -> ArgParser class instance
        (input) data -> Dictionary that has package data
        (output) status -> Tuple on operation status
            status[0] - True|False - Successful operation
            status[1] - Error message

    """

    status = (True, None)
    status2 = rabbitmq_publish(args, data)

    if not status2[0]:
        status = (status2[0], status2[1])

    indent = None if args.get_val("-f", def_val=False) else 4
    data = json.dumps(data, indent=indent)
    write_file(args, data)
    display_data(args, data)
    mail_data(args, data)

    return status


def kernel_run(args, dnf):

    """Function:  kernel_run

    Description:  Checks to see if the kernel check can be done and process
        the output.

    Note:  This is only available for the Dnf class use.

    Arguments:
        (input) args -> ArgParser class instance
        (input) dnf -> Dnf class instance
        (output) status -> Tuple on operation status
            status[0] - True|False - Successful operation
            status[1] - Error message

    """

    status, data = kernel_check(dnf)

    if status[0]:
        status = output_run(args, data)

    return status


def run_program(args, func_dict):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.

    Arguments:
        (input) args -> ArgParser class instance
        (input) func_dict -> Dictionary list of functions and options

    """

    func_dict = dict(func_dict)
    dnf = gen_dnf.Dnf()

    # Intersect args.args_array & func_dict to find which functions to call.
    for item in set(args.get_args_keys()) & set(func_dict.keys()):
        status = func_dict[item](args, dnf)

        if not status[0]:
            print(f"Error Detected: {status[1]}")


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_perms_chk -> contains directories and their octal permissions
        file_perms_chk -> contains file names and their octal permissions
        file_crt -> contains options which require files to be created
        func_dict -> dictionary list for the function calls or other options
        opt_con_req_dict -> contains the options that require other options
        opt_multi_list -> contains the options that will have multiple values
        opt_val_list -> contains options which require values

    Arguments:
        (input) argv -> Arguments from the command line

    """

    dir_perms_chk = {"-d": 5}
    file_perms_chk = {"-o": 6}
    file_crt = ["-o"]
    func_dict = {"-L": list_ins_pkg, "-U": list_upd_pkg, "-R": list_repo,
                 "-K": kernel_run}
    opt_con_req_dict = {"-s": ["-e"], "-u": ["-e"], "-r": ["-b", "-d"]}
    opt_multi_list = ["-e", "-s"]
    opt_val_list = ["-b", "-d", "-o", "-e", "-s", "-y"]

    # Process argument list from command line.
    args = gen_class.ArgParser(
        sys.argv, opt_val=opt_val_list, multi_val=opt_multi_list)

    if args.arg_parse2()                                                    \
       and not gen_libs.help_func(args, __version__, help_message)          \
       and args.arg_cond_req_or(opt_con_or=opt_con_req_dict)                \
       and args.arg_dir_chk(dir_perms_chk=dir_perms_chk)                    \
       and args.arg_file_chk(file_perm_chk=file_perms_chk, file_crt=file_crt):

        try:
            proglock = gen_class.ProgramLock(
                sys.argv, args.get_val("-y", def_val=""))
            run_program(args, func_dict)
            del proglock

        except gen_class.SingleInstanceException:
            print(f'WARNING:  Lock in place for package_admin with id of:'
                  f' {args.get_val("-y", def_val="")}')


if __name__ == "__main__":
    sys.exit(main())
