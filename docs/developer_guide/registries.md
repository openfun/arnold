# Using private Docker registries

To get deployed, your application may need to pull a Docker image stored in a
private Docker registry. Fortunately, Arnold supports this common scenario.

## Create OKD Secret that stores Docker registry credentials

First, you will need to declare the credentials to login to this private
registry in a dedicated Ansible vault with the following expected path:

```
group_vars/customer/{{ customer }}/{{ env_type }}/secrets/registries.vault.yml
```

This vault should contain a list of Docker registries with the following
format:

```yaml
# Docker private registries
registries:
  - name: foo
    server: https://foo.com
    username: foo
    password: pass

  - name: bar
    server: https://bar.com
    username: bar
    password: pass
```

Once edited, don't forget to encrypt it _via_:

```
$ bin/run ansible-vault encrypt \
    group_vars/customer/{{ customer }}/{{ env_type }}/secrets/registries.vault.yml
```

Now you'll be able to create the corresponding secrets with the
`create_secrets.yml` playbook (for more details see the [secrets
documentation](./secrets.md)):

```
$ bin/ansible-playbook --ask-vault-pass create_secrets.yml
```

## Use Docker registry secret

Now that your secret has been created, you can use it in your jobs or deployment
configurations using the `imagePullSecrets` field in your `spec`:

```yaml
apiVersion: v1
kind: DeploymentConfig
# [...]
spec:
  template:
    spec:
      imagePullSecrets:
        - name: foo
```

The name of this pull secret should match the name of your registry in the
registries list.
