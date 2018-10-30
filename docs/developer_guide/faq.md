# Frequently Asked Questions

## How can I login to the web console with an administrator account?

```bash
# Login as a system administrator account
$ oc login -u system:admin

# Add cluster-admin role to the admin user
$ oc adm policy add-cluster-role-to-user cluster-admin admin

# Now login as admin should be allowed
$ oc login -u admin
```

## OpenShift's Docker registry is refusing connections, what can I do?

Most of the time, it means that the Docker registry pod is down or has failed to
deploy. Once OpenShift is running, login to the web console with an
administrator account (see previous question), and restart the deployment of the
`docker-registry` app in the `default` namespace / project.

> **TODO**: add the corresponding `oc` command

## Running pods are not resolving domain names properly, what can I do?

OpenShift's default DNS servers are copied by `oc` from the host configuration
(`/etc/resolv.conf` file). If your system is driven by `systemd`, the default
name server (_e.g._ `127.0.0.53`), has no meaning in a Docker context. So, you
will need to stop the cluster (`oc cluster down`), update the content of the
`openshift.local.clusterup/kubedns/resolv.conf` file with the below example
configuration and then restart the cluster (`bin/dev`).

```conf
# openshift.local.clusterup/kubedns/resolv.conf
# Point to Google's DNS (or any other public DNS)
nameserver 8.8.8.8
nameserver 8.8.4.4
```
