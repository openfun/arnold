# Arnold

[![CircleCI](https://circleci.com/gh/openfun/arnold.svg?style=svg)](https://circleci.com/gh/openfun/arnold)

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
changes to your OpenShift instance that orchestrates your OpenEdx services.

## Requirements

* [Docker](https://docs.docker.com/engine/installation/): we use docker to
  develop and run Arnold. This is a strict requirement to use this project.
* [OpenShift](https://docs.openshift.org/latest/welcome/index.html) (or
  [MiniShift](https://docs.openshift.org/latest/minishift/getting-started/)): as
  Arnold should talk with someone, you'll need a running OpenShift instance to
  use this project. For development or demo purposes, please read our
  [instructions to install MiniShift](./docs/installation/minishift.md) on your machine in a
  few minutes.

## Quick start

> Disclaimer: this quick start guide has been written with development / testing
> purpose in mind. If you are looking for more insights on how to use it in
> production, please refer to our [documentation](./docs/index.md).

First things first: you'll need to clone this repository to start playing with
Arnold:

```bash
$ cd path/to/working/directory
$ git clone git@github.com:openfun/arnold.git
```

As we heavily rely on Ansible and OpenShift, we've cooked a Docker container
image that bundles Ansible and the OpenShift CLI (you have already installed
Docker on your machine right?). You can build this image with a little helper we
provide:

```bash
$ cd path/to/cloned/repo
$ bin/build
```

If everything goes well, you must have built Arnold's Docker image. You can
check its availability _via_:

```bash
$ docker images arnold
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
arnold              0.1.0-alpha         549baa2b861b        4 days ago          824MB
```

Second requirement: you'll need to ensure that you have a working OpenShift
instance that will be used to deploy your services. For development or testing
purpose, we recommend you to install and start a MiniShift (see Arnold's
[documentation](./docs/installation/minishift.md)).

Now that you have a working OpenShift, let's have fun (sic!) by creating a project for a customer
in a particular environment with a new helper:

> When running this command, you'll be asked for a **vault password**. The
> default value for this demo is: `arnold`.

```bash
$ bin/init
```

Tadaaa! Arnold has created a new OpenShift project called `patient0-development`
with a collection of services up and running.

Note that the `edxapp-dbmigrate-init` job may take some time. When it has
completed successfully, you can create a demo course and some users by running:

```bash
$ bin/ansible-playbook load_fixtures.yml
```

The following users will be created:

| username | password | email               | is staff | is superuser |
|---------:|:--------:|:-------------------:|:--------:|:------------:|
| student  | student  | student@example.com | no       | no           |
| teacher  | teacher  | teacher@example.com | no       | no           |
| staff    | staff    | staff@example.com   | yes      | no           |
| admin    | admin    | admin@example.com   | yes      | yes          |


You could also try deploying the same services for another customer and/or environment by
overriding the default Ansible variables:

```bash
$ bin/init -e "env_type=staging customer=campus"
```

If you want to run a new deployment for this project, there is also a helper for
that:

```bash
$ bin/deploy
```

As we are using a blue-green deployment strategy, you should now have two
running versions of each service, congratulations! 🎉🎉🎉

If everything goes well, maybe you are convinced by Arnold and you want to use
it at home. In this case, we invite you to start reading the project's
documentation (see below).

## Documentation

The full documentation of the project is available in this repository (see
[./docs](./docs)) (and also in readthedocs soon).

## Contributing

Please, see the [CONTRIBUTING](CONTRIBUTING.md) file.

## Contributor Code of Conduct

Please note that this project is released with a [Contributor Code of
Conduct](http://contributor-covenant.org/). By participating in this project you
agree to abide by its terms. See [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md) file.

## License

The code in this repository is licensed under the MIT license terms unless
otherwise noted.

Please see `LICENSE` for details.
