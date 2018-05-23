# Requirements

## Docker

We use [Docker](https://www.docker.com) to develop and run Arnold. You will need
to install it on your system following the official documentation:
https://docs.docker.com/engine/installation/

If you already have installed Docker, make sure it is a recent release
(`>=17.12`).

## OpenShift (or MiniShift for development)

As Arnold will deploy dockerized applications to OpenShift, make sure you have a
fully functional OpenShift console where you can log in.

> If you intend to test Arnold or work on it, we recommend to install MiniShift
> on your machine (see [Install MiniShift](./minishift.md) section from our
> documentation).

If you plan to work with a remote dedicated OpenShift console, you need to
install a recent release of the `oc` client (`>=3.9`).

It can be downloaded from the [GitHub releases
page](https://github.com/openshift/origin/releases) of the project's repository.
Once downloaded, untar the archive and copy the `oc` binary somewhere in your
`$PATH` (_e.g._ `$HOME/bin`).

Check that your `oc` client is ready to talk to your OpenShift console _via_:

```bash
# login to OpenShift console
$ oc login https://openshift.mydomain.com:8443 --username=foo --password=xxx
```

with:

* `openshift.mydomain.com`: the domain name pointing to your running OpenShift
  console
* `foo`: your console login (account)
* `xxx`: your console account password

> If you are asked to use an "insecure connection" (because "the server uses a
> certificate signed by an unknown authority") and you are running on our
> OpenShift's pre-production instance, you can safely accept.
