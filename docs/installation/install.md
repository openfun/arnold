# Install & configure Arnold

Before starting this installation procedure, please make sure you fulfill project requirements (see [requirements section](./requirements.md)).

## Install Arnold

First things first: you'll need to clone Arnold's repository to start playing
with it:

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

## Configure Arnold

When running sugar scripts in the `bin/` directory, Arnold's docker image is
implicitly run with environment variables as defined in `env.d/development`.

If you need to customize the environment variables used, you need to create a custom
file:

```bash
# Create a production environment from the default "development" environment
$ cp env.d/development env.d/production

# Edit this file to suite your needs
$ vim env.d/production
```

All environment files except `development` are git ignored as they may contain sensitive
information.

> Note that the `K8S_AUTH_API_KEY` and `K8S_AUTH_HOST` vars can be left empty
> for development as they are dynamically defined in our sugar scripts but need to
> be set in the environment file for a securized OpenShift instance.

You can then specify the environment file when running a sugar script by setting the
`env-file` option as in the following example:

```bash
$ bin/bootstrap --env-file=env.d/production
```
