# Arnold

[![CircleCI](https://circleci.com/gh/openfun/arnold.svg?style=svg)](https://circleci.com/gh/openfun/arnold)

Arnold is a generic tool to deploy dockerized applications to
[Kubernetes](https://kubernetes.io/) with [Ansible](https://www.ansible.com). It was built
by France Université Numérique to ease its infrastructure deployment.

## Overview

Arnold has been designed as a suite of Ansible playbooks and Kubernetes object
definition templates (Jinja2). We take advantage of the `k8s` Ansible modules
to make Ansible talk with Kubernetes.

## Requirements

- [Docker](https://docs.docker.com/engine/installation/): we use docker to
  develop and run Arnold. This is a strict requirement to use this project.
- [Kubectl](https://kubernetes.io/docs/tasks/tools/):
  This CLI is used to communicate with the running Kubernetes instance you
  will use.

Optionally:

- [k3d](https://k3d.io/): This tool is used to setup and run a lightweight
  Kubernetes cluster, in order to have a local environment (it is required to
  complete below's quickstart instructions to avoid depending on an existing
  Kubernetes cluster).
- [gnupg](https://gnupg.org/) to encrypt Ansible vaults passwords and
  collaborate with your team.
- [curl](https://curl.se/) to download and install Arnold's CLI.

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
example, we consider that you want to create a namespace for the `hd-inc`
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

You can start a local development cluster using the `make cluster` command.

After a while, a local k3d cluster should be up and running.


It's time to create our new project and deploy the hello application!

> The bootstrap command will ask your confirmation to create a new project,
> please proceed by pressing the enter key from your keyboard.

```bash
$ arnold -c hd-inc -e development bootstrap
```

And voilà! You have deployed your first application in a k8s project using
Arnold 🎉

We can check that our pods are running using the `kubectl` CLI:

```bash
# List created pods
$ kubectl get pods -n development-hd-inc
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

As we heavily rely on Ansible and Kubernetes, we've cooked a Docker container
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

### Run a local Kubernetes cluster

You'll need to ensure that you have Kubernetes instance that will be used to
deploy your services. For development or testing purpose, we recommend you to
use the `make cluster` command to start a local minimalist cluster to work with
(don't do it now, please read the next paragraph first).

Before starting the cluster, make sure that your system meets the following
requirements:

1. To run ElasticSearch (you'll probably have an application that will use it),
   you will need to ensure that your kernel's `vm.max_map_count` parameter is
   at least `262144`:

```bash
$ sudo sysctl -w vm/max_map_count=262144
```

Now that you've configured your system, you can safely start a cluster _via_:

```bash
$ make cluster
```

### Deploy!

Now that you have a working Kubernetes cluster, let's have fun (sic!) by
creating a project for a customer in a particular environment with the `arnold`
script:

```bash
# Activate development environment
$ source bin/activate

# Run the bootstrap command for the eugene customer in development environment
$ bin/arnold -c eugene -e development -a hello bootstrap
```

Tadaaa! Arnold has created a new Kubernetes namespace called `eugene-development` with
the `hello` application up and running. You can check this using the `oc` CLI:

```bash
# List namespaces
$ kubectl get namespace

# Get created pods
$ kubectl get pods -n eugene-development
```

### Going further

By following this quick start guide, you only scratched the surface of
Arnold's capabilities. We invite you to read the project's
[documentation](./docs) (see below), to know more about Arnold's core
features such as:

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
