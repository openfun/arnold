# MiniShift

Minishift is a tool that helps you run OpenShift locally by running a
single-node OpenShift cluster inside a VM. We recommend you to install it to
test Arnold or work on it.


## Pre-requisite: install & configure an hypervisor

MiniShift needs an hypervisor to work with: it uses KVM by default by can also run on
[VirtualBox](https://www.virtualbox.org/wiki/Downloads).

We recommend using VirtualBox because developers are more likely to have it on their
laptops and we encountered networking issues with KVM.

If you have already installed and configured VirtualBox (or KVM), you can safely skip
this section.


### Using VirtualBox

Using VirtualBox is pretty straight forward: we invite you to follow
installation instructions from the [official project
page](https://www.virtualbox.org/).

️⚠️️⚠️️️⚠️️ **Important notice** ⚠️️⚠️️⚠️️

When you first start `minishift` (see below), it will create a `minishift`
virtual machine (VM). To increase overall performances, we strongly invite you
to start the VirtualBox GUI and make the following changes:

1.  change the network adapter from its default (_Intel PRO/1000 MT Desktop_) to
    **PCnet-FAST III**.
2.  allocate at least **4Gb base memory**


### Using KVM as hypervisor

```bash
# Install kvm
$ sudo apt install libvirt-bin qemu-kvm

# Add yourself to the libvirt group to avoid having to use sudo
$ sudo usermod -a -G libvirt $(whoami)

# Update your current session to take into account this new group
$ newgrp libvirt

# Create & start a default network (required for minishift)
# see: https://wiki.libvirt.org/page/Networking
$ sudo virsh net-define /etc/libvirt/qemu/networks/default.xml
$ sudo virsh net-autostart default
$ sudo virsh net-start default

# Install docker-machine
$ DOCKER_MACHINE_RELEASE="0.14.0"
$ curl -L "https://github.com/docker/machine/releases/download/v${DOCKER_MACHINE_RELEASE}/docker-machine-$(uname -s)-$(uname -m)" -o /tmp/docker-machine
$ chmod +x /tmp/docker-machine
$ sudo cp /tmp/docker-machine /usr/local/bin/docker-machine

# Install kvm driver
$ DOCKER_MACHINE_KVM_DRIVER_RELEASE="0.7.0"
$ curl -L "https://github.com/dhiltgen/docker-machine-kvm/releases/download/v${DOCKER_MACHINE_KVM_DRIVER_RELEASE}/docker-machine-driver-kvm" -o /tmp/docker-machine-driver-kvm
$ chmod +x /tmp/docker-machine-driver-kvm
$ sudo cp /tmp/docker-machine-driver-kvm /usr/local/bin/docker-machine-driver-kvm
```

_nota bene_: if for some reasons, you cannot find the default network
configuration on your system (`/etc/libvirt/qemu/networks/default.xml` for
ubuntu), you can create it with the following content:

```xml
<!-- /etc/libvirt/qemu/networks/default.xml -->
<network>
  <name>default</name>
  <!-- feel free to generate a new uuid via uuidgen -->
  <uuid>74996da2-ade7-4a28-b87e-4fb121fbfb29</uuid>
  <forward mode='nat'/>
  <!-- you may need to adapt the bridge name to your configuration, e.g. virbr1 -->
  <bridge name='virbr0' stp='on' delay='0'/>
  <!-- you can generate a random mac address here -->
  <mac address='52:54:00:fd:6e:bf'/>
  <ip address='192.168.122.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.122.2' end='192.168.122.254'/>
    </dhcp>
  </ip>
</network>
```


## Installing MiniShift

For **GNU/Linux**:

```bash
# See latest releases at:
# https://github.com/minishift/minishift/releases
$ MS_RELEASE="1.17.0"
$ curl -L "https://github.com/minishift/minishift/releases/download/v${MS_RELEASE}/minishift-${MS_RELEASE}-linux-amd64.tgz" -o /tmp/minishift-${MS_RELEASE}-linux-amd64.tgz
$ cd /tmp
$ tar xvzf /tmp/minishift-${MS_RELEASE}-linux-amd64.tgz
$ sudo cp /tmp/minishift-${MS_RELEASE}-linux-amd64/minishift /usr/local/bin/minishift
$ cd -
$ rm -Rf /tmp/minishift*
```

For other systems like **MacOSX** or **Windows**, please refer to the official
MiniShift documentation:
https://docs.openshift.org/latest/minishift/getting-started/installing.html

## Getting started with MiniShift

Let's test our installation and login to MiniShift's console _via_ the `oc login` command.
This can be achieved with a helper:

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
exception to for the missing SSL certificate, login with **developer**
credentials (see `minishift` output above) and be amazed by OpenShift web
console.


## Direct commands

The bin/dev script is just a wrapper to start MiniShift and login to its OC CLI. You can start
MiniShift directly with the following commands:

```bash
$ minishift start --memory=4GB [--vm-driver=virtualbox]
```

> Nota bene: if you are using VirtualBox as hypervisor, you will need to add the
> `--vm-driver=virtualbox` option to the `start` command.

When using virtualbox as hypervisor, the `memory` option will only be effective the first time you
start MiniShift (when the VM is created in VirtualBox). 4GB is the minimum required to play
Open edX's database migrations. If you encounter issues running such migrations, check in
VirtualBox that MiniShift has enough RAM allocated.


When starting `MiniShift` for the first time, it will install the latest release
of `oc` (OpenShift CLI) for you. To add `oc` to your `$PATH`, ask minishift:

```bash
# Ask minishift which path should be added to $PATH
$ minishift oc-env
export PATH="/home/user/.minishift/cache/oc/v3.9.0/linux:$PATH"

# Now run this command to add "oc" to $PATH in the current shell
$ export PATH="/home/user/.minishift/cache/oc/v3.9.0/linux:$PATH"
```

You can then login to the MiniShift OC CLI directly with the following command:

```bash
$ oc login "https://$(minishift ip):8443" --username=developer --password=developer
```
