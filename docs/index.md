# Arnold

Arnold is a tool to deploy dockerized applications to
[OpenShift](https://www.openshift.com/) with
[Ansible](https://www.ansible.com/). It was built by France Université Numérique
to ease its infrastructure deployment.

The current work mainly focuses on the [Open edX MOOC
platform](https://open.edx.org/), but it can be considered as a generic tool to
deploy your dockerized applications.

## Overview

Arnold has been designed as a suite of Ansible playbooks and OpenShift object
definition templates (Jinja2). We take advantage of the `openshift_raw` Ansible
module to make Ansible talk with OpenShift.

As a DevOps using this project, you will need to adapt OpenShift object
templates to suite your needs or constraints and run playbooks to push your
changes to your OpenShift instance that orchestrate your OpenEdx services.

## Documentation

### I. Installation

1.  [Requirements](./installation/requirements.md)
2.  [Install MiniShift](./installation/minishift.md)
3.  [Install & configure Arnold](./installation/install.md)

### II. Developer guide

1.  [Concepts overview](./developer_guide/concepts.md)
2.  [Getting started](./developer_guide/getting_started.md)
3.  [Using Ansible playbooks](./developer_guide/playbooks.md)
4.  [Working with routes](./developer_guide/routes_aliases.md)
5.  [Handling secrets](./developer_guide/secrets.md)
6.  [Hello customer](./developer_guide/hello.md)

### III. Contributing

1.  [Guide lines](../CONTRIBUTING.md)
2.  [Best practices](./contributing/best_practices.md)
3.  [Naming conventions](./contributing/naming_conventions.md)
