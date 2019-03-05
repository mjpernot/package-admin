# Python project for the administration of Linux packages.
# Classification (U)

# Description:
  This program is used to adminstrate packages on a Linux server.  This will include detecting packages requiring to be updated and reporting on these packages via JSON and/or Mongo database entries.


#####  This README file is broken down into the following sections:
  * Features
  * Prerequisites
  * Installation
  * Configuration
  * Program Description
  * Program Help Function
  * Help Message
  * Testing
    - Unit
    - Integration
    - Blackbox


# Features:
  * Listing current packages requiring to be updated.
  * Listing current repositories.
  * List all packages currently installed on the server.
  * Save results to file and/or Mongo database.


# Prerequisites:
  * List of Linux packages that need to be installed on the serveri via git.
    - python-libs
    - python-devel
    - git
    - python-pip

  * Local class/library dependencies within the program structure.
    - lib/gen_class
    - lib/arg_parser
    - lib/gen_libs
    - mongo_lib/mongo_libs


# Installation:

Install these programs using git.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
umask 022
cd {Python_Project}
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/package-admin.git
```

Install/upgrade system modules.

```
cd package-admin
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Configuration (optional):
  * Configuration file is only required if you want to insert the output of package_admin.py into a Mongo database.

Create Mongo configuration file.

```
cd config
cp mongo.py.TEMPLATE mongo.py
```

Make the appropriate change to the Mongo environment depending on either a single Mongo database setup or Mongo replica set setup.

Single Mongo database.  Change the variables to reflect a single Mongo database environment.
  * Change these entries in the mongo.py file.
    - user = "USER"
    - passwd = "PASSWORD"
    - host = "IP_ADDRESS"
    - name = "HOSTNAME"

```
vim mongo.py
chmod 600 mongo.py
```

Mongo replica set.  Change the variables to reflect a Mongo replica set environment.
  * Change these entries in the mongo.py file.
    - user = "USER"
    - passwd = "PASSWORD"
    - host = "IP_ADDRESS"
    - name = "HOSTNAME"
    - repset = "REPLICA_SET_NAME"
    - repset_hosts = "HOST1:PORT, HOST2:PORT, [...]"
    - db_auth = "AUTHENTICATION_DATABASE"

```
vim mongo.py
chmod 600 mongo.py
```


# Program Description:
### Program:  package_admin.py
##### Description:  Linux Package administration program for handling packages on a Linux server.


# Program Help Function:

  All of the programs, except the command and class files, will have an -h (Help option) that will show display a help message for that particular program.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
{Python_Project}/package-admin/package_admin.py -h
```


# Help Message:
  Below is the help message for the program the program.  Run the program with the -h option get the latest help message for the program.

    Program:      package_admin.py

    Description:  Linux Package administration program for handling packages on
        a Linux server.  This program has a number of functions to include
        listing current packages, listing any new package updates, installing
        package updates, and listing current repositories.

    Usage:
        package_admin.py {-L | -U | -R} {-j}
            {-i db_name:table_name -c file -d path} {-v | -h}

    Arguments:
        -L => List all packages installed on the server.
        -U => List update packages awaiting for the server.
        -R => List current repositories.
        -j => Return output in JSON format.
        -i {database:collection} => Name of database and collection to
            insert the database statistics data into.  Available for -U option.
            Requires options:  -c and -d
            Default:  sysmon:server_pkgs
        -c file => Mongo server configuration file.  Required for -i option.
        -d dir path => Directory path to config file (-c).  Required for -i
            option.
        -n => No standard.  Do not send output to standard out.
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


# Testing:

# Unit Testing:

### Description: Testing consists of unit testing for the functions in the package_admin.py program.

### Installation:
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

Install these programs using git.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/package-admin.git
```

Install/upgrade system modules.

```
cd package-admin
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Unit test runs for package_admin.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/package-admin
```

### Unit:  help_message

```
test/unit/package_admin/help_message.py
```

### Unit:  process_yum

```
test/unit/package_admin/process_yum.py
```

### Unit:  list_upd_pkg

```
test/unit/package_admin/list_upd_pkg.py
```

### Unit:  list_ins_pkg

```
test/unit/package_admin/list_ins_pkg.py
```

### Unit:  list_repo

```
test/unit/package_admin/list_repo.py
```

### Unit:  run_program

```
test/unit/package_admin/run_program.py
```

### Unit:  main

```
test/unit/package_admin/main.py
```

### All unit testing

```
test/unit/package_admin/unit_test_run.sh
```

### Code coverage for unit testing

```
test/unit/package_admin/code_coverage.sh
```


# Integration Testing:

### Description: Testing consists of integration testing of functions in the package_admin.py program.

### Installation:
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

Install these programs using git.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/package-admin.git
```

Install/upgrade system modules.

```
cd package-admin
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

### Configuration:

Create Mongo configuration file.

```
cd test/integration/package_admin/config
cp ../../../../config/mongo.py.TEMPLATE mongo.py
```

Change the variables to reflect the integration test environment setup.  Make the appropriate change to the Mongo environment depending on either a single Mongo database setup or Mongo replica set setup.

Single Mongo database.  Change the variables to reflect a single Mongo database environment.
  * Change these entries in the mongo.py file:
    - user = "USER"
    - passwd = "PASSWORD"
    - host = "IP_ADDRESS"
    - name = "HOSTNAME"

```
vim mongo.py
chmod 600 mongo.py
```

Mongo replica set.  Change the variables to reflect a Mongo replica set environment.
  * Change these entries in the mongo.py file:
    - user = "USER"
    - passwd = "PASSWORD"
    - host = "IP_ADDRESS"
    - name = "HOSTNAME"
    - repset = "REPLICA_SET_NAME"
    - repset_hosts = "HOST1:PORT, HOST2:PORT, [...]"
    - db_auth = "AUTHENTICATION_DATABASE"

```
vim mongo.py
chmod 600 mongo.py
```

# Integration test runs for package-admin.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/package_admin
```

### Integration:  process_yum

```
test/integration/package_admin/process_yum.py
```

### Integration:  list_upd_pkg

```
test/integration/package_admin/list_upd_pkg.py
```

### Integration:  list_ins_pkg

```
test/integration/package_admin/list_ins_pkg.py
```

### Integration:  list_repo

```
test/integration/package_admin/list_repo.py
```

### Integration:  run_program

```
test/integration/package_admin/run_program.py
```

### Integration:  main

```
test/integration/package_admin/main.py
```

### All integration testing

```
test/integration/package_admin/integration_test_run.sh
```

### Code coverage for integration testing

```
test/integration/package_admin/code_coverage.sh
```


# Blackbox Testing:

### Description: Testing consists of blackbox testing of the package-admin.py program.

### Installation:
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

Install these programs using git.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/package-admin.git
```

Install/upgrade system modules.

```
cd package-admin
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

### Configuration:

Create Mongo configuration file.

```
cd test/blackbox/package_admin/config
cp ../../../../config/mongo.py.TEMPLATE mongo.py
```

Change the variables to reflect the integration test environment setup.  Make the appropriate change to the Mongo environment depending on either a single Mongo database setup or Mongo replica set setup.

Single Mongo database.  Change the variables to reflect a single Mongo database environment.
  * Change these entries in the elastic.py file:
    - user = "USER"
    - passwd = "PASSWORD"
    - host = "IP_ADDRESS"
    - name = "HOSTNAME"

```
vim mongo.py
chmod 600 mongo.py
```

Mongo replica set.  Change the variables to reflect a Mongo replica set environment.
  * Change these entries in the elastic.py file:
    - user = "USER"
    - passwd = "PASSWORD"
    - host = "IP_ADDRESS"
    - name = "HOSTNAME"
    - repset = "REPLICA_SET_NAME"
    - repset_hosts = "HOST1:PORT, HOST2:PORT, [...]"
    - db_auth = "AUTHENTICATION_DATABASE"

```
vim mongo.py
chmod 600 mongo.py
```

# Blackbox test run for package-admin.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/package_admin
```

### Blackbox:  

```
sudo test/blackbox/package_admin/blackbox_test.sh
```

