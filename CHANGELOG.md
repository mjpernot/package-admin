# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


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
- list_upd_pkg, list_ins_pkg, list_repo, process_yum:  Changed output to camelCase.
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

