# Getting started

Now that Docker, OpenShift (or MiniShift) and Arnold are installed and
functional on your system, it's time to play!

> **Disclaimer**: the following tutorial has been written using MiniShift in
> development environment. We will update this documentation soon for production
> environments.

## Using development environment

Before running our first playbook, we need to start MiniShift and login to
MiniShift's console _via_ the `oc login` command. This can be achieved with a
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

## Using native Docker commands

As you may have noticed, our sugar scripts wrap `docker run` calls running
Ansible commands in Arnold's docker image. Their purpose is to ease the
developer experience and help docker beginners to test the project. Those sugar
scripts only works with a "local" minishift instance. If you want to use Arnold
with a real OpenShift instance, at the time of writing, you will need to be more
comfortable with docker to run Arnold.

An example call to play with a remote OpenShift console follows:

```bash
# Make sure the env.d/production file defines the K8S_AUTH_HOST environment variable
# and that your already logged in to the OpenShift console _via_ `oc login`
$ docker run --rm -it \
    --env-file env.d/production \
    --env K8S_AUTH_API_KEY=$(oc whoami -t) \
    arnold \
    ansible-playbook init_project.yml -e "env_type=production customer=patient0"
```

This command will run the `init_project.yml` Ansible playbook with the
`-e "env_type=production customer=patient0"` argument that defines Ansible vars
for this run.

Another more complexe example to use `ansible-vault` follows:

```bash
$ docker run --rm -it \
    -u $(id -u) \
    -v $PWD:/app \
    --env-file env.d/production \
    arnold \
    ansible-vault decrypt --ask-vault-pass \
        group_vars/secret/patient0/development/edxapp/credentials.vault.yml
```

This command runs `ansible-vault` to decrypt credentials stored in a vaulted
file. As by default, the credentials file will be decrypted in the container, we
will not be able to get the resulting file if we do not use a docker volume.
Hence, we need to change de container running user ID with the host user ID
(`-u $(id -u)`) and mount the current host directory in the container's `/app`
directory (`-v $PWD:/app`).
