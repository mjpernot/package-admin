# Python project for the administration of Linux packages.
# Classification (U)

# Description:
  Linux Package administration program for handling packages on a Linux server that uses yum.  This program is used to adminstrate packages on a Linux server.  This will include detecting packages requiring to be updated and reporting on these packages via JSON and/or Mongo database entries.


#####  This README file is broken down into the following sections:
  * Features
  * Prerequisites
    - FIPS Environment
  * Installation
  * Configuration
  * Program Help Function
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
    - git
    - python-pip
    - python-devel

  * Local class/library dependencies within the program structure.
    - python-lib
    - mongo-lib

  * FIPS Environment:  If operating in a FIPS 104-2 environment, this package will require at least a minimum of pymongo==3.8.0 or better.  It will also require a manual change to the auth.py module in the pymongo package.  See below for changes to auth.py.  In addition, other modules may require to have the same modification as the auth.py module.  If a stacktrace occurs and it states "= hashlib.md5()" is the problem, then note the module name "= hashlib.md5()" is in and make the same change as in auth.py:  "usedforsecurity=False".
    - Locate the auth.py file python installed packages on the system in the pymongo package directory.
    - Edit the file and locate the \_password_digest function.
    - In the \_password_digest function there is an line that should match: "md5hash = hashlib.md5()".  Change it to "md5hash = hashlib.md5(usedforsecurity=False)".
    - Lastly, it will require the configuration file entry auth_mech to be set to: SCRAM-SHA-1 or SCRAM-SHA-256.

  *  If the platform is Redhat 8 and above, list of Linux packages that need to be installed on the server.
    - dnf==4.7.0

# Installation:

Install these programs using git.
  * From here on out, any reference to **{Python_Project}** or **PYTHON_PROJECT** replace with the baseline path of the python program.

```
umask 022
cd {Python_Project}
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/package-admin.git
```

Install/upgrade system modules.

Centos 7 (Running Python 2.7):

```
sudo pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```

Redhat 8 (Running Python 3.6):
NOTE: Install as the user that will run the program.

```
python -m pip install --user -r requirements3.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```

Install supporting classes and libraries.

Centos 7 (Running Python 2.7):

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

Redhat 8 (Running Python 3.6):

```
python -m pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mongo-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Mongo Configuration (optional):
  * Mongo configuration file is only required if you want to insert the output of package_admin.py into a Mongo database.

Create Mongo configuration file.  Make the appropriate change to the environment.
  * Make the appropriate changes to connect to a Mongo database.
    - user = "USER"
    - japd = "PSWORD"
    - host = "HOST_IP"
    - name = "HOSTNAME"

  * Change these entries only if required:
    - port = 27017
    - conf_file = None
    - auth = True
    - auth_db = "admin"
    - auth_mech = "SCRAM-SHA-1"

  * Notes for auth_mech configuration entry:
    - NOTE 1:  SCRAM-SHA-256 only works for Mongodb 4.0 and better.
    - NOTE 2:  FIPS 140-2 environment requires SCRAM-SHA-1 or SCRAM-SHA-256.
    - NOTE 3:  MONGODB-CR is not supported in Mongodb 4.0 and better.

  * If connecting to a Mongo replica set, otherwise set to None.
    - repset = "REPLICA_SET_NAME"
    - repset_hosts = "HOST_1:PORT, HOST_2:PORT, ..."
    - db_auth = "AUTHENTICATION_DATABASE"

  * If using SSL connections then set one or more of the following entries.  This will automatically enable SSL connections. Below are the configuration settings for SSL connections.  See configuration file for details on each entry:
    - ssl_client_ca = None
    - ssl_client_key = None
    - ssl_client_cert = None
    - ssl_client_phrase = None

```
cd config
cp mongo.py.TEMPLATE mongo.py
vim mongo.py
chmod 600 mongo.py
```


# RabbitMQ Configuration (optional):
  * RabbitMQ configuration file is only required if you want to publish the output of package_admin.py into RabbitMQ.

Create RabbitMQ configuration file.  Make the appropriate change to the environment.
  * Make the appropriate changes to connect to a RabbitMQ database.
    - user = "USER"
    - japd = "PSWORD"
    - host = "HOSTNAME"
    - host_list = []
    - queue = "QUEUENAME"
    - r_key = "ROUTING_KEY"
    - exchange_name = "EXCHANGE_NAME"
  * Do not change this section unless you have knowledge with RabbitMQ.
    - port = 5672
    - exchange_type = "direct"
    - x_durable = True
    - q_durable = True
    - auto_delete = False

```
cd config
cp rabbitmq.py.TEMPLATE rabbitmq.py
vim rabbitmq.py
chmod 600 rabbitmq.py
```


# Program Help Function:

  All of the programs, except the command and class files, will have an -h (Help option) that will show display a help message for that particular program.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:

```
{Python_Project}/package-admin/package_admin.py -h
```


# Testing:

# Unit Testing:

### Installation:

Install the project using the procedures in the Installation section.

### Testing:

```
cd {Python_Project}/package-admin
test/unit/package_admin/unit_test_run.sh
```

### Code coverage:

```
cd {Python_Project}/package-admin
test/unit/package_admin/code_coverage.sh
```


# Integration Testing:

### Installation:

Install the project using the procedures in the Installation section.

### Configuration:

Configure the project using the procedures in the Configuration section.
  * Exception:  The location of the configuration file will be different, see below.

```
cd test/integration/package_admin/config
cp ../../../../config/mongo.py.TEMPLATE mongo.py
vim mongo.py
chmod 600 mongo.py
```

### Testing:

```
cd {Python_Project}/package_admin
test/integration/package_admin/integration_test_run.sh
```

### Code coverage:

```
cd {Python_Project}/package_admin
test/integration/package_admin/code_coverage.sh
```


# Blackbox Testing:

### Installation:

Install the project using the procedures in the Installation section.

### Configuration:

Configure the project using the procedures in the Configuration section.
  * Exception:  The location of the configuration file will be different, see below.

```
cd test/blackbox/package_admin/config
cp ../../../../config/mongo.py.TEMPLATE mongo.py
vim mongo.py
chmod 600 mongo.py
```

### Testing:

```
cd {Python_Project}/package_admin
test/blackbox/package_admin/blackbox_test.sh
```

