# Getting started

Now that Docker, OpenShift (or MiniShift) and Arnold are installed and
functional on your system, it's time to play!


## Using development environment

Now let's have fun (sic!) by creating an OpenShift project for a customer in a
particular environment with a new helper:

> When running this command, you'll be asked for a **vault password**. The
> default value for this demo is: `arnold`.

```bash
$ bin/bootstrap
```

Tadaaa! Arnold has created a new OpenShift project called `eugene-development`
with a collection of services up and running. You can change the customer /
environment to deploy by overriding default environment variables:

```bash
$ bin/bootstrap -e "env_type=staging customer=campus"
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
    ansible-playbook bootstrap.yml -e "env_type=production customer=eugene"
```

This command will run the `bootstrap.yml` Ansible playbook with the
`-e "env_type=production customer=eugene"` argument that defines Ansible vars
for this run.

Another more complexe example to use `ansible-vault` follows:

```bash
$ docker run --rm -it \
    -u $(id -u) \
    -v $PWD:/app \
    --env-file env.d/production \
    arnold \
    ansible-vault decrypt --ask-vault-pass \
        group_vars/secret/eugene/development/edxapp/credentials.vault.yml
```

This command runs `ansible-vault` to decrypt credentials stored in a vaulted
file. As by default, the credentials file will be decrypted in the container, we
will not be able to get the resulting file if we do not use a docker volume.
Hence, we need to change de container running user ID with the host user ID
(`-u $(id -u)`) and mount the current host directory in the container's `/app`
directory (`-v $PWD:/app`).
