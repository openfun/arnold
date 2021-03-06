# Ansible playbooks

Arnold is composed of a suite of playbooks and OpenShift templates to create
various objects representing services. In this section, we will list and
describe all playbooks bundled with Arnold. We choose to describe them in the
order they are supposed to be used.

> **Remark**: when running an Ansible playbook, you can pass arguments to
> override Ansible variables definition (_e.g._ `ansible-playbook my_playbook.yml -e "my_var=my_value"` to define `my_var` with the `my_value`
> value in executed playbook). Hence, every time you see the `-e` option for a
> playbook invocation, it means that we will override default values. You must
> know that default values for `customer` and `env_type` are `eugene` and
> `development` respectively. **In all cases, the `-e "customer=foo env_type=bar"` option is not required if you want to work with `eugene` in
> `development`**.

## `create_databases_vault.yml`

This playbook will generate credentials for the databases required by active applications.
Every application should describe its own required databases. To do so, create a `databases.yml` file in the `apps/{{ app.name }}/vars` directory with the following content:

```yaml
databases:
  - engine: "mysql"
    release: "5.7"
  - engine: "mongodb"
    release: "3.2"
```

_nota bene_: `engine` and `release` are mandatories parameters.

Please note that this playbook works in "append" mode, _i.e._ existing `databases` vault will never be erased nor existing databases credentials modified. If you add a new application that requires databases, you can safely run this playbook again and new databases credentials will be configured.

### Usage

You don't need to be connected to your OpenShift instance to run this playbook.

```bash
$ bin/run ansible-playbook create_databases_vault.yml --ask-vault-pass
```

## `delete_project.yml`

This playbook deletes a project with all OpenShift objects for a customer
(default: `eugene`) in a particular environment (default: `development`).

### Usage

```bash
# development
$ bin/ansible-playbook delete_project.yml -e "customer=eugene env_type=staging"

# native command for production
$ docker run --rm -it \
    --env-file env.d/production \
    arnold \
    ansible-playbook delete_project.yml -e "customer=eugene env_type=staging"
```

## `bootstrap.yml`

This playbook is a "meta" playbook that creates a new project with all required
OpenShift objects for a customer (default: `eugene`) in a particular
environment (default: `development`).
It executes sequentially the following playbooks:

- `delete_project.yml`
- `init_project.yml`
- `deploy.yml`

### Usage

```bash
# sugar development
$ bin/bootstrap

# development
$ bin/ansible-playbook bootstrap.yml -e "customer=eugene env_type=staging"

# native command for production
$ docker run --rm -it \
    --env-file env.d/production \
    arnold \
    ansible-playbook bootstrap.yml -e "customer=eugene env_type=staging"
```

## `init_project.yml`

This playbook is a "meta" playbook that creates a new project with all required
OpenShift objects for a customer (default: `eugene`) in a particular environment
(default: `development`).

It executes sequentially the following playbooks:

- `create_project.yml`
- `create_volumes.yml`
- `create_htpasswds.yml` (when `activate_http_basic_auth` is true)
- `create_secrets.yml`
- `create_acme.yml`
- `create_routes.yml`

### Usage

```bash
# sugar development
$ bin/init

# development
$ bin/ansible-playbook init_project.yml -e "customer=eugene env_type=staging"

# native command for production
$ docker run --rm -it \
    --env-file env.d/production \
    arnold \
    ansible-playbook init_project.yml -e "customer=eugene env_type=staging"
```

## `deploy.yml`

The `deploy.yml` playbook defines a new `deployment_stamp` to create a whole new
stack by defining OpenShift objects with unique labels and names. This allows us
to initiate a blue/green deployment strategy.

### Usage

```bash
# development
$ bin/ansible-playbook deploy.yml -e "customer=eugene env_type=staging"

# native command for production
$ docker run --rm -it \
    --env-file env.d/production \
    arnold \
    ansible-playbook deploy.yml -e "customer=eugene env_type=staging"
```

## `switch.yml`

The `switch.yml` playbook moves:

1. the _current_ stack to the _previous_ route
2. the _next_ stack to the _current_ route.

_nota bene_: the `apps_filter` environment variable definition is required to
ensure that you are switching a blue-green compatible application that has been
recently deployed to the next stack.

### Usage

```bash
# sugar development
$ bin/switch -e "customer=eugene env_type=staging apps_filter=richie"

# development
$ bin/ansible-playbook switch.yml \
    -e "customer=eugene env_type=staging apps_filter=richie"

# native command for production
$ docker run --rm -it \
    --env-file env.d/production \
    arnold \
    ansible-playbook switch.yml \
        -e "customer=eugene env_type=staging apps_filter=richie"
```

## `create_project.yml`

This playbook only creates a new OpenShift project name defined with the
following pattern: `{{ env_type }}-{{ customer }}`

### Usage

```bash
# development
$ bin/ansible-playbook create_project.yml -e "customer=eugene env_type=staging"

# native command for production
$ docker run --rm -it \
    --env-file env.d/production \
    arnold \
    ansible-playbook create_project.yml -e "customer=eugene env_type=staging"
```

## `create_secrets.yml`

The `create_secrets.yml` playbook creates OpenShift secrets that may store
sensitive credentials. It uses vaulted Yaml definition files stored in
`group_vars/secrets/{{ customer }}/{{ env_type }}/*/credentials.vault.yml` to
create those secrets. It must be invoked with the `--ask-vault-pass` option so
that Ansible can decrypt vaulted credentials and push secrets to OpenShift.

### Usage

```bash
# development
$ bin/ansible-playbook create_secrets.yml --ask-vault-pass -e "customer=eugene env_type=staging"

# native command for production
$ docker run --rm -it \
    --env-file env.d/production \
    arnold \
    ansible-playbook create_secrets.yml --ask-vault-pass -e "customer=eugene env_type=staging"
```

## `create_acme.yml`

We use this playbook to automatically generate [Let's
Encrypt](https://letsencrypt.org) SSL certificates for every deployment (if the
current `env_type` is not `development`). The certificates issued are
automatically renewed by the service running to OpenShift.

### Usage

```bash
# development
$ bin/ansible-playbook create_acme.yml -e "customer=eugene env_type=staging"

# native command for production
$ docker run --rm -it \
    --env-file env.d/production \
    arnold \
    ansible-playbook create_acme.yml -e "customer=eugene env_type=staging"
```

## `create_object.yml`

This playbook is mostly used in development to create or update an OpenShift
object we are working on.

### Usage

```bash
# development
$ bin/ansible-playbook create_object.yml -e "customer=eugene env_type=staging" \
        -e "object_template=templates/openshift/edxapp/job/import_demo_course.yml.j2"

# native command for production
$ docker run --rm -it \
    --env-file env.d/production \
    arnold \
    ansible-playbook create_object.yml -e "customer=eugene env_type=staging" \
        -e "object_template=templates/openshift/edxapp/job/import_demo_course.yml.j2"
```

## `create_vaults.yml`

This playbook will be used to create the vault files needed by an application. It will read the databases vault
and creates the vault application based on its template (`app/{app.name}/vars/vault/main.yml.j2`).

Note that this playbook requires the databases.vault.yml vault as input to generate applications vaults. We expect this vault to be in `groups_vars/customers/{{ customer }}/{{ env_type }}/secrets/databases.vault.yml`.

### Usage

You don't need to be connected to an OpenShift instance to run this playbook.

```bash
$ bin/run ansible-playbook create_vaults.yml --ask-vault-pass
```

## `create_routes.yml`

This playbook creates routes for all active applications and redirections (if
any).

### Usage

```bash
$ bin/run ansible-playbook create_routes.yml
```
