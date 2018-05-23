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

## Requirements

* [Docker](https://docs.docker.com/engine/installation/): we use docker to
  develop and run Arnold. This is a strict requirement to use this project.
* [OpenShift](https://docs.openshift.org/latest/welcome/index.html) (or
  [MiniShift](https://docs.openshift.org/latest/minishift/getting-started/)): as
  Arnold should talk with someone, you'll need a running OpenShift instance to
  use this project. For development or demo purpose, please read our
  [instructions to install MiniShift](./docs/minishift.md) on your machine in a
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

Second requirement: you'll need to ensure that you have a working OpenShift
instance that will be used to deploy our services. For development or testing
purpose, we recommend you to install MiniShift (see Arnold's
[documentation](./docs/minishift.md)).

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

When we will use sugar scripts in the `bin/` directory, we will implicitly run
Arnold's docker image loading the `env.d/development` environment variables
definition. We need to create this file from the `env.d/base` template:

```bash
# Create development environment variables definition from base template
$ cp env.d/base env.d/development

# Edit this file to suite your needs
$ vim env.d/development
```

> Note that the `K8S_AUTH_API_KEY` and `K8S_AUTH_HOST` vars can be left empty
> for development as they are dynamically defined in our sugar scripts.

Before running our first playbook, we need to start MiniShift and login to
MiniShift's console _via_ the `oc login` command. This can be achieve with a
second helper:

```bash
$ bin/dev
```

Once executed, the `bin/dev` script should print the local OpenShift console URL
and default credentials to login:

```
**** MiniShift is up and running ****
local console: https://192.168.99.100:8443
username: developer
password: developer

To login as administrator, use:
$ oc login -u system:admin
***************************************
```

Open your web browser with the console url (_e.g._ something similar to
[https://192.168.99.100:8443](https://192.168.99.100:8443)), add a security
exception to for the missing SSL certificate, login and be amazed by OpenShift
web console.

Now let's have fun (sic!) by creating an OpenShift project for a customer in a
particular environment with a new helper:

```bash
$ bin/init
```

Tadaaa! Arnold has created a new OpenShift project called `patient0-development`
with a collection of services up and running. You can change the customer /
environment to deploy by overriding default environment variables:

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
