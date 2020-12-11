# Arnold

[![CircleCI](https://circleci.com/gh/openfun/arnold.svg?style=svg)](https://circleci.com/gh/openfun/arnold)

Arnold is a generic tool to deploy dockerized applications to
[OKD](https://www.okd.io) (_aka_ the Community Distribution of Kubernetes that
powers Red Hat OpenShift) with [Ansible](https://www.ansible.com). It was built
by France Université Numérique to ease its infrastructure deployment.

## Overview

Arnold has been designed as a suite of Ansible playbooks and OpenShift object
definition templates (Jinja2). We take advantage of the `k8s` Ansible modules
to make Ansible talk with OKD.

## Requirements

- [Docker](https://docs.docker.com/engine/installation/): we use docker to
  develop and run Arnold. This is a strict requirement to use this project.
- [OpenShift's client](https://docs.openshift.org/latest/welcome/index.html)
  (_aka_ `oc`): this CLI is used to communicate with the running OpenShift
  instance you will use. Plus, it offers the possibility to run a minimal
  cluster for development purpose (using a set of docker containers). You
  can use the [`3.11` release of
  `oc`](https://github.com/openshift/origin/releases/tag/v3.11.0). Please
  avoid the `3.10` release because we encountered DNS issues with it.

Optionally:

- [curl](https://curl.se/) to download and install Arnold's CLI.
- [gnupg](https://gnupg.org/) to encrypt Ansible vaults passwords and
  collaborate with your team.

## Quick start for Arnold's users

### Install Arnold

Arnold is a shell script that can be downloaded from its repository and
installed somewhere in your `$PATH`. In the following, we choose to install it
in the user space using the `${HOME}/.local/bin` directory:

```bash
# Download & install Arnold script somewhere in your ${PATH}
$ mkdir -p ${HOME}/.local/bin/ && \
    curl https://raw.githubusercontent.com/openfun/arnold/master/bin/arnold > ${HOME}/.local/bin/arnold && \
    chmod +x ${HOME}/.local/bin/arnold
```

If the `${HOME}/.local/bin` directory is not in your `${PATH}`, you can add it
by editing your shell configuration file (`${HOME}/.bashrc` or
`${HOME}/.zshrc`) and copy/paste the following `export` command:

```bash
# Add this to your shell configuration (if not already done)
export PATH="${HOME}/.local/bin:${PATH}"
```

### Bootstrap a project

Arnold provides a command to setup a new project from scratch. In the following
example, we consider that you want to create a project for the `hd-inc`
customer (_aka_ Happy Days Incorporated) in a `development` environment (you
will find more details on the customer and environment concepts in the
[documentation](./docs)).

```bash
# Create the project's directory
$ mkdir myproject && cd myproject
$ arnold -c hd-inc -e development setup
```

Your project's tree should look like a base Ansible's project:

```
.
└── group_vars
    ├── common
    └── customer
        └── hd-inc
            ├── development
            │   ├── main.yml
            │   └── secrets
            │       └── databases.vault.yml
            └── main.yml

6 directories, 3 files
```

We will now edit our customer definition file to describe which application we
want to deploy:

```yaml
# group_vars/customer/hd-inc/main.yml
#
#
# Variables specific to the hd-inc customer
project_display_name: "Happy Days Incorporated ({{ env_type }})"
project_description: "HD-Inc applications in {{ env_type }} environment."

apps:
  - name: hello
```

If you don't have a configured openshift cluster that can be used for your
tests, you can start a local development cluster using the `oc cluster`
command:

```bash
# Start a local development cluster (optional)
$ export K8S_DOMAIN="$(hostname -I | awk '{print $1}')"
$ oc cluster up --server-loglevel=5 --public-hostname=${K8S_DOMAIN}
```

After a while, a local k8s cluster should be up and running. It's time to login
to this local cluster in insecure mode:

```bash
$ oc login "https://${K8S_DOMAIN}:8443" -u developer -p developer --insecure-skip-tls-verify=true
```

> If you use a remote cluster, you should also login to this cluster using the
> `oc login` command. Feel free to adapt options depending on your own
> configuration.

It's time to create our new project and deploy the hello application!

> The bootstrap command will ask your confirmation to create a new project,
> please proceed by pressing the enter key from your keyboard.

```bash
# If you use a local cluster, the SSL certificate verification will fail, you
# should then define the K8S_AUTH_VERIFY_SSL environment variable and set it
# to "no".
$ export K8S_AUTH_VERIFY_SSL="no"

$ arnold -c hd-inc -e development bootstrap
```

And voilà! You have deployed your first application in a k8s project using
Arnold 🎉

We can check that our pods are running using the `oc` CLI:

```bash
# Switch to the newly created project
$ oc project development-hd-inc

# List created pods
$ oc get pods
```

The output should look like the following:

```
NAME                     READY     STATUS    RESTARTS   AGE
redirect-nginx-1-qrmrd   1/1       Running   0          4m
```

Our pod is running. Yata!

Arnold offers many more refinements and possibilities. We invite you to read
our [documentation](./docs) to explore Arnold's features and dig deeper in its
usage.

## Quick start for Arnold's developers

### Build Arnold

First things first: you'll need to clone this repository to start playing with
Arnold:

```bash
$ cd path/to/working/directory
$ git clone git@github.com:openfun/arnold.git
```

As we heavily rely on Ansible and OKD (k8s), we've cooked a Docker container
image that bundles Ansible and Arnold's playbooks (you have already installed
Docker on your machine right?). You can build this image with a little helper
we provide:

```bash
$ cd arnold
$ make build && make build-dev
```

If everything goes well, you must have built Arnold's Docker images. You can
check their availability _via_:

```bash
$ docker images arnold
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
arnold              5.21.2              0d37702fd3e8        4 days ago          322MB
arnold              5.21.2-dev          cd799128fbf6        4 days ago          370MB
```

While the development image (noted `5.21.2-dev` in this build) contains
development tools (quality checks as linters and test runners), the production
image (noted `5.21.2` in this build) only contains Ansible and Arnold's
playbooks.

### Run a local OpenShift cluster

You'll need to ensure that you have an OKD (k8s) instance that will be used to
deploy your services. For development or testing purpose, we recommend you to
use the `make cluster` command to start a local minimalist cluster to work with
(don't do it now, please read the next paragraph first).

Before starting the cluster, make sure that your system meets the following
requirements:

1. Make sure that the `/etc/docker/daemon.json` file contains at list
   `172.30.0.0/16` as insecure registry:

```json
{
  "insecure-registries": ["172.30.0.0/16"]
}
```

2. To run ElasticSearch (you'll probably have an application that will use it),
   you will need to ensure that your kernel's `vm.max_map_count` parameter is
   at least `262144`:

```bash
$ sudo sysctl -w vm/max_map_count=262144
```

Now that you've configured your system, you can safely start a cluster _via_:

```bash
$ make cluster
```

If everything goes well, you can start a web browser with the following address
to access the web console: https://192.168.1.10:8443 (replace `192.168.1.10`
with your local IP).

You can log in the web console with `developer` as your username **and**
password.

> _nota bene_: you'll probably be asked to accept the connection even if it is
> insecure (SSL certificate issue). Please do so.

### Deploy!

Now that you have a working OKD cluster, let's have fun (sic!) by creating a
project for a customer in a particular environment with the `arnold` script:

```bash
# Activate development environment
$ source bin/activate

# Run the bootstrap command for the eugene customer in development environment
$ bin/arnold -c eugene -e development -a hello bootstrap
```

Tadaaa! Arnold has created a new OKD project called `eugene-development` with
the `hello` application up and running. You can check this using the `oc` CLI:

```bash
# List projects
$ oc projects

# Activate the newly created project
$ oc project eugene-development

# Get created pods
$ oc get pods
```

### Going further

By following this quick start, you only scratched the surface of Arnold's
capabilities. We invite you to read the project's [documentation](./docs) (see
below), to know more about Arnold's core features such as:

- multiple client/environment configurations support
- blue/green deployment strategy
- application discovery (add your own applications easily)
- ...

## Documentation

The full documentation of the project is available in this repository (see
[./docs](./docs)) (and also in readthedocs soon).

## Contributing

Please, see the [CONTRIBUTING](CONTRIBUTING.md) file.

## Contributor Code of Conduct

Please note that this project is released with a [Contributor Code of
Conduct](http://contributor-covenant.org/). By participating in this project
you agree to abide by its terms. See [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md)
file.

## License

The code in this repository is licensed under the MIT license terms unless
otherwise noted.

Please see `LICENSE` for details.
