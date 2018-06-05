# Handling project secrets

Arnold uses OpenShift's `Secret` objects to securely inject services credentials
to running pods. Those `Secret`s are generated from an encrypted YAML file that
defines secret values (`credentials.vault.yml`) and a `Secret` object template
(see `templates/openshift/common/secret/env_vars.yml.j2`).

The encrypted YAML files are expected to be stored in:

```
group_vars/secret/{{ customer }}/{{ env_type }}/{{ application }}/credentials.vault.yml
```

Credentials files are securely encrypted using the `ansible-vault` tool before
being versioned in Arnold's repository (see usage in the next sections). In
plain text, the `credentials.vault.yml` file looks like:

```yaml
# customer: patient0
# env_type: staging

# centos/postgresql-96-centos7 image environment
POSTGRESQL_USER: foo
POSTGRESQL_PASSWORD: pass

# application's environment
DJANGO_SECRET_KEY: fakekey

# We can also store complex values such as dictionaries...
FOO_DICT:
    - first_key: "bar"
    - second_key: "baz"

# ...or lists
FOO_LIST:
    - "bar"
    - "baz"
    - "spam"
```

## Generate a new secret

Once you have generated a plain text YAML file with required credentials for
your application (see example above), you will need to encrypt its content,
version it and create or update secrets in OpenShift:

```bash
# Encrypt plain text credentials
# Nota bene: you'll be asked to type the encryption password twice
$ bin/run ansible-vault encrypt --ask-vault-pass path/to/credentials.vault.yaml

# Add the file to the repository
$ git add path/to/credentials.vault.yaml
$ git commit -m "Add new secret for foo app"

# Create or update the secret in OpenShift for the
# "Patient 0" customer in "development" env_type.
$ bin/ansible-playbook --ask-vault-pass create_secrets.yml

# Alternatively, if you want to create a secret for
# another customer/env_type
$ bin/ansible-playbook --ask-vault-pass create_secrets.yml \
    -e "customer=corporate" -e "env_type=staging"
```

> TODO: for production examples, use raw docker commands instead of the sugar
> scripts

## Update a secret

To allow different versions of a `Secret` for a deployed application, `Secret`s
have a `secret_id` attached to them and linked to DCs and jobs (see
`group_vars/all/main.yml`).

### Override a secret

In case you need to override a secret (because of a typo in a password, etc.),
here is the recipe to follow:

```bash
# Edit the credentials
$ bin/run ansible-vault edit --ask-vault-pass path/to/credentials.vault.yaml

# Commit changes
$ git add path/to/credentials.vault.yaml
$ git commit -m "Update secrets for foo app"

# Update secrets
$ bin/ansible-playbook --ask-vault-pass create_secrets.yml

# Alternatively, if you want to update secrets for another
# customer/env_type
$ bin/ansible-playbook --ask-vault-pass create_secrets.yml \
    -e "customer=corporate" -e "env_type=staging"
```

Updating a secret should raise a signal that re-deploys automatically all your
DCs depending on this particular secret.

### Create a new version of the secret

When you want to create a new secret and keep compatibility with previously
deployed secrets, we recommend you to upgrade the `secret_id` variable in
`group_vars/all/main.yml` (this variable follows a semantic versioning schema),
create the new secrets and then start a new deployment of your application.

```bash
# Edit the credentials
$ bin/run ansible-vault edit --ask-vault-pass path/to/credentials.vault.yaml

# Update secret version
$ grep secret_id group_vars/all/main.yml
secret_id: "1.0.0"

$ vim group_vars/all/main.yml

$ grep secret_id group_vars/all/main.yml
secret_id: "1.1.0"

# Commit changes
$ git add group_vars/all/main.yml path/to/credentials.vault.yaml
$ git commit -m "Update secrets for foo app"

# Create a new version of the secrets
$ bin/ansible-playbook --ask-vault-pass create_secrets.yml

# Deploy
$ bin/deploy

# Alternatively, if you want to create a new version of
# the secrets for another customer/env_type
$ bin/ansible-playbook --ask-vault-pass create_secrets.yml \
    -e "customer=corporate" -e "env_type=staging"

$ bin/deploy -e "customer=corporate" -e "env_type=staging"
```
