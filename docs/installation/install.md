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

**TODO**

* improve the documentation and this feature for other environments (staging,
  production, etc.)
