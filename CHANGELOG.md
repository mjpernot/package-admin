# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [3.1.0] - 2025-07-15
- Add ability to send email data as an file attachment.
- Updated python-lib v4.0.3
- Updated rabbitmq-lib v2.4.1

### Changed
- mail_data: Added ability to email data out as a file attachment.
- main: Added -j and -g options to allow for email attachments.
- Documentation changes.


## [3.0.0] - 2025-01-07
Breaking Changes

- Removed support for Python 2.7.
- Removed mongo insert (-i) option.
- Updated urllib3==1.26.20
- Added certifi==2024.12.14
- Updated python-lib==4.0.0
- Updated rabbitmq-lib==2.3.0

### Fixed
- main: Added -b to opt_val_list to ensure rabbitmq file name is passed.

### Changed
- run_program: Replaced gen_class.Dnf with gen_dnf.Dnf.
- kernel_run, run_program: Removed Python 2.7 code.
- get_installed_kernels, kernel_check: Replaced dict() with {} and list() with [].
- process_yum, output_run, run_program, main: Removed mongo code.
- main, run_program: Converted strings to f-strings.
- Documentation changes.

### Removed
- Removed mongo_insert function.
- Removed mongo_lib library.
- Removed distro module.
- Removed dnf module.


## [2.6.11] - 2024-11-15

### Fixed
- Set chardet==3.0.4 for Python 3.

### Deprecated
- Support for Python 2.7


## [2.6.10] - 2024-10-29
- Updated chardet==4.0.0 for Python 3.
- Updated distro==1.9.0 for Python 3.
- Added idna==2.10 for Python 3.
- Updated pika==1.3.1 for Python 3.
- Updated psutil==5.9.4 for Python 3.
- Updated requests==2.25.0 for Python 3.
- Updated urllib3==1.26.19 for Python 3.
- Updated python-lib to v3.0.7.
- Updated rabbitmq-lib to v2.2.7.
- Updated mongo-lib to v4.3.3.

### Changed
- Updates to requirements3.txt.
- Documentation updates.


## [2.6.9] - 2024-09-27
- Updated pymongo==4.1.1 for Python 3.6
- Updated simplejson=3.13.2 for Python 3
- Updated python-lib to v3.0.5


## [2.6.8] - 2024-08-07
- Updated requests==2.25.0
- Added idna==2.10

### Changed
- Updates to requirements.txt.


## [2.6.7] - 2024-08-02
- Added idna==2.8 for Python 2.
- Added certifi==2019.11.28 for Python 2.
- Set simplejson==3.13.2


## [2.6.6] - 2024-07-31
- Removed email from requirement packages.


## [2.6.5] - 2024-07-29
- Set urllib3 to 1.26.19 for Python 2 for security reasons.
- Updated rabbitmq-lib to v2.2.4

### Fixed
- list_upd_pkg: Only allow kernel_check call if on Python 3 or better.


## [2.6.4] - 2024-06-27

### Fixed
- kernel_check: Changed RebootRequired values from True|False to Yes|No due to json.dumps issue with boolean case.

### Changed
- output_run: Reverted the changes from the previous version v2.6.3 back to v2.6.2.


## [2.6.3] - 2024-06-24

### Fixed
- output_run: Retain the Boolean value properly in the dictionary for emailing purposes (i.e. RabbitMQ/rmq-sysmon).

### Changed
- main: Removed parsing from gen_class.ArgParser call and called arg_parse2 as part of "if" statement.
- Documentation updates.


## [2.6.2] - 2024-04-23
- Updated mongo-lib to v4.3.0
- Added TLS capability for Mongo
- Set pymongo to 3.12.3 for Python 2 and Python 3.

### Changed
- Set pymongo to 3.12.3 for Python 2 and Python 3.
- config/mongo.py.TEMPLATE: Added TLS entries.
- Documentation updates.


## [2.6.1] - 2024-02-21
- Updated module requirements for Python

### Changed
- Set simplejson to 3.12.0 for Python 3.
- Set chardet to 3.0.4 for Python 2 and Python 3.
- Added urllib3 set to 1.24.2 for Python 2 and 3.


## [2.6.0] - 2024-02-06
- Added option to determine if server requires a reboot based on current and installed kernel.
- Updated python-lib to v3.0.2

### Added
- kernel_run: Checks to see if the kernel check can be done and process the output.
- kernel_check: Compares the current running kernel version to the latest kernel installed version.
- get_latest_kernel: Return the latest kernel version.
- get_running_kernel: Return the running kernel version.
- get_installed_kernels: Return the installed kernel versions on the server.
- create_template_dict: Set up dictionary with server-level details.
- mongo_insert: Insert data into MongoDB.
- rabbitmq_publish: Publish data to RabbitMQ.
- write_file: Write data to a file.
- display_data: Display data to terminal.
- mail_data: Email data out.
- output_run: Directs where the data output will go.

### Changed
- list_upd_pkg: Refactored the function to use the new functions added instead of process_yum.
- Documentation updates.


## [2.5.0] - 2024-01-18
- Updated to work in Python 3 too
- Added Dnf class to work on RedHat 8 servers
- Updated to work in Red Hat 8
- Updated python-lib to v3.0.1
- Updated mongo-lib to v4.2.8
- Updated rabbitmq-lib to v2.2.2

### Changed
- run_program: Determine whether to initialize a Yum class or Dnf class based on python version used.
- Documentation updates.


## [2.4.0] - 2023-06-14
- Upgrade python-lib to v2.10.1
- Replace arg_parser.arg_parse2 with gen_class.ArgParser.
- Added ability (-r option) to publish to RabbitMQ.
- No longer support Python 2.6

### Added
- config/rabbitmq.py.TEMPLATE: RabbitMQ configuration file.

### Changed
- process_yum: Added check for -r option to publish to RabbitMQ. 
- Multiple functions: Replaced the arg_parser code with gen_class.ArgParser code.
- Documentation updates.


## [2.3.4] - 2022-12-01
- Released pulled.


## [2.3.3] - 2022-06-28
- Upgrade mongo-libs to v4.2.1
- Upgrade python-lib to v2.9.2

### Changed
- config/mongo.py.TEMPLATE: Removed old entries.
- Documentation updates.


## [2.3.2] - ???
### Changed
- process_yum:  Refactored function to reduce number of assignment statements.
- config/mongo.py.TEMPLATE: Added SSL configuration entries.
- Documentation update.


## [2.3.1] - 2020-02-16

### Fixed
- Allow to override the default sendmail (postfix) and use mailx command.

### Changed
- process_yum:  Determine whether to use sendmail or mailx when using the mail option.
- main:  Added -u option to allow override of sendmail and use mailx.
- Removed \*\*kwargs from function argument lists that do not require it.
- Documentation update.


## [2.3.0] - 2021-01-22
- Changed -n with -z option to standardize among the other programs.
- Added -a option to append to a file.

### Fixed
- process_yum:  Replaced -j option with -f option to flatten JSON document.

### Changed
- process_yum:  Added -a option to allow for appending of data to a file.
- process_yum:  Changed -n with -z option.
- main:  Added program lock to running the run_program call.
- run_program:  Captured and process status from function calls.
- list_upd_pkg, list_ins_pkg, list_repo:  Capture and process status from process_yum function.
- process_yum:  Capture and process status from Mongo insert connection.
- config/mongo.py.TEMPLATE:  Add authentication mechanism entries.
- list_upd_pkg, list_ins_pkg, list_repo, process_yum:  Converted dictionary keys to PascalCase.
- Documentation updates.

### Added
- Added Program lock capability.


## [2.2.0] - 2020-06-26
### Fixed
- main:  Fixed handling command line arguments from SonarQube scan finding.

### Added
- Added email capability to program.

### Changed
- process_yum:  Added email capability for output.
- main:  Added email options to the setup.
- config/mongo.py.TEMPLATE: Changed format of the Mongo connection.


## [2.1.7] - 2019-09-26
### Changed
- process_yum:  Replaced "gen_libs.data_multi_out" with own internal code.
- Documentation update.


## [2.1.6] - 2019-05-14
### Fixed
- list_repo, list_ins_pkg, list_upd_pkg, process_yum, run_program:  Fixed problem with mutable default arguments issue.


## [2.1.5] - 2019-03-06
### Changed
- list_upd_pkg, list_ins_pkg, list_repo, process_yum:  Changed output to PascalCase.
- main: Refactored code to bring into standard convention.


## [2.1.4] - 2018-11-01
- Tested on Python 2.7.

### Changed
- list_upd_pkg, list_ins_pkg, list_repo, run_program, process_yum:  Changed Yum instance name from "YUM" to "yum".
- Documentation updates.


## [2.1.3] - 2018-06-01
### Changed
- Documentation updates.


## [2.1.2] - 2018-05-30
### Changed
- process_yum:  Changed OS_Release tag in "data" variable to return OS distribution data.


## [2.1.1] - 2018-04-10
### Changed
- Documentation updates.


## [2.1.0] - 2018-04-05
### Changed
- main:  Changed library references for "arg_parser" and "gen_libs" to new naming schema.
- process_yum:  Added OS release to output.
- Changed from "system" reference to "gen_class" reference.
- run_program: Changed library references for "gen_libs" to new naming schema.
- run_program:  Changed from "system" reference to "gen_class" reference.


## [2.0.2] - 2018-04-02
### Changed
- Documentation updates.

 
## [2.0.1] - 2018-03-21
### Changed
- Documentation updates


## [2.0.0] - 2018-03-20
Breaking Change

### Changed
- main:  Removed "opt_xor_dict" and "gen_libs.Arg_Xor_Dict" call.
- main:  Removed "-j" from the required options list.
- main:  Removed "-I" from the list of options to select.
- process_yum: Changed "gen_libs.JSON_2_Out" to "gen_libs.ins_doc".
- process_yum: Changed "gen_libs.Print_Dict" to "gen_libs.data_multi_out".
- Updated help message on the Mongo configuration file layout.
- Changed import library from "cmds_mongo" to "mongo_libs".
- process_yum:  Changed library from "cmds_mongo" to "mongo_libs".
- help_message:  Standardized the argument call.
- process_yum:  Refactored code on "\*\*kwargs" arguments parsing.
- Changed function names from uppercase to lowercase.
- Moved Mongo support libraries to "mongo_lib" directory.
- Setup single-source version control.

### Removed
- update_pkg function - as it is yet to be implemented.
- Removed "lib.errors" library module.


## [1.3.0] - 2018-02-28
### Added
- Added single-source version control.


## [1.2.0] - 2017-08-15
### Changed
- Change versioning information.
- Change single quotes to double quotes.
- Changed to use local libraries from ./lib directory.
- Help_Message:  Replace docstring with printing the programs \_\_doc\_\_.


## [1.1.0] - 2017-08-14
### Changed
- Process_Yum: Add call to insert data into Mongo database.
- Process_Yum: Replace call to Dict_Out with Print_Dict and error checking.


## [1.0.0] - 2016-06-13
- Initial creation of program.

