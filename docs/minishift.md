# MiniShift

## Pre-requisite: install & configure an hypervisor

MiniShift needs an hypervisor to work with. The following documentation focuses
on the installation of KVM as it's MiniShift's default hypervisor, but know that
[VirtualBox](https://www.virtualbox.org/wiki/Downloads) is also supported. If
you have already installed and configured KVM (or VirtualBox), you can safely
skip this section.

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
$ curl -L https://github.com/docker/machine/releases/download/v${DOCKER_MACHINE_RELEASE}/docker-machine-`uname -s`-`uname -m` -o /tmp/docker-machine
$ chmod +x /tmp/docker-machine
$ sudo cp /tmp/docker-machine /usr/local/bin/docker-machine

# Install kvm driver
$ DOCKER_MACHINE_KVM_DRIVER_RELEASE="0.7.0"
$ curl -L https://github.com/dhiltgen/docker-machine-kvm/releases/download/v${DOCKER_MACHINE_KVM_DRIVER_RELEASE}/docker-machine-driver-kvm -o /tmp/docker-machine-driver-kvm
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

### Using VirtualBox

Using VirtualBox is pretty straight forward: we invite you to follow
installation instructions from the [official project
page](https://www.virtualbox.org/).

**Important notice**

When you first start `minishift` (see below), it will create a `minishift`
virtual machine (VM). To increase network performance, we strongly invite you to
start the VirtualBox GUI and change the network adapter from its default (_Intel
PRO/1000 MT Desktop_) to **PCnet-FAST III**.

## Install MiniShift

For ubuntu:

```bash
# See latest releases at:
# https://github.com/minishift/minishift/releases
$ MS_RELEASE="1.16.0"
$ curl -L https://github.com/minishift/minishift/releases/download/v${MS_RELEASE}/minishift-${MS_RELEASE}-linux-amd64.tgz -o /tmp/minishift-${MS_RELEASE}-linux-amd64.tgz
$ pushd /tmp
$ tar xvzf /tmp/minishift-${MS_RELEASE}-linux-amd64.tgz
$ sudo cp /tmp/minishift-${MS_RELEASE}-linux-amd64/minishift /usr/local/bin/minishift
$ popd
$ rm -Rf /tmp/minishift*
```

## Getting started with MiniShift

Let's test our MiniShift installation:

```bash
$ minishift start [--vm-driver=virtualbox]
```

> Nota bene: if you are using VirtualBox as hypervisor, you will need to add the
> `--vm-driver=virtualbox` option to the `start` command.

When starting `minishift` for the first time, it will install the latest release
of `oc` (OpenShift CLI) for you. To add it to your `$PATH`, add the following
line to your `.bashrc` or `.zshrc`:

```bash
# Add oc to the $PATH
eval $(minishift oc-env)
```
