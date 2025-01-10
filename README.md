# Python project for the administration of Linux packages.
# Classification (U)

# Description:
  Linux Package administration program for handling packages on a Linux server that uses yum.  This program is used to adminstrate packages on a Linux server.  This will include detecting packages requiring to be updated and reporting on these packages via JSON.


#####  This README file is broken down into the following sections:
  * Features
  * Prerequisites
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


# Prerequisites:
  * List of Linux packages that need to be installed on the serveri via git.
    - python3-devel
    - python3-pip
    - gcc
    - dnf


# Installation:

Install these programs using git.

```
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/package-admin.git
cd package-admin
```

Install/upgrade system modules.

NOTE: Install as the user that will run the program.

```
python -m pip install --user -r requirements3.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```

Install supporting classes and libraries.

```
python -m pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-rabbitmq-lib.txt --target rabbit_lib --trusted-host pypi.appdev.proj.coe.ic.gov
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
cp config/rabbitmq.py.TEMPLATE config/rabbitmq.py
vim config/rabbitmq.py
chmod 600 config/rabbitmq.py
```


# Program Help Function:

  All of the programs, except the command and class files, will have an -h (Help option) that will show display a help message for that particular program.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:

```
package-admin/package_admin.py -h
```


# Testing:

# Unit Testing:

### Installation:

Install the project using the procedures in the Installation section.

### Testing:

```
test/unit/package_admin/unit_test_run.sh
test/unit/package_admin/code_coverage.sh
```


# Integration Testing:

### Installation:

Install the project using the procedures in the Installation section.

### Testing:

```
test/integration/package_admin/integration_test_run.sh
test/integration/package_admin/code_coverage.sh
```


# Blackbox Testing:

### Installation:

Install the project using the procedures in the Installation section.

### Testing:

```
test/blackbox/package_admin/blackbox_test.sh
```

