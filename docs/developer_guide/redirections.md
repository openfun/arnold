# HTTP Redirections

Arnold is shipped with a "redirect" core application that provides an easy way
to set HTTP redirections for OpenShift hosted services. Of course, this can be
setup in many other ways outside from your OpenShift's projects, but we think
it's pretty neat to empower project's developers by allowing them to redirect
inbound traffic from one route to another with a single variable configuration.

## Method

The "redirect" application is deployed during the project's initialization (see
the `init_project.yml` playbook). This app is based on a single deployment and
service based on NGINX to perform redirections. Based on a single configuration
(the `redirections` variable, see next section), the `create_redirect.yml`
playbook will create an NGINX configuration and the corresponding routes (one
per redirection).

## Usage

> **Disclaimer:** for each URL that must be redirected, you will need to add a
> DNS record that points to your OpenShift server.

To declare redirections for a customer in a particular environment, you should
edit the project's variable definition (`main.yml`) and configure the
`redirections` list. An example follows for the `eugene` customer in `staging`
environment.

```yaml
# group_vars/customer/eugene/staging/main.yml

# [...]
redirections:
  - to: "www.richie.{{ env_type }}.{{ domain_name }}"
    from:
      - "richie.{{ env_type }}.{{ domain_name }}"
      - "richie.{{ domain_name }}/staging/"
  - to: "www.marsha.{{ env_type }}.{{ domain_name }}"
    from:
      - "marsha.{{ env_type }}.{{ domain_name }}"
```

In this example, we redirect all `from` URL definitions to the `to` URL, _e.g._
richie.staging.foo.com and richie.foo.com/staging to www.richie.staging.foo.com,
and marsha.staging.foo.com to www.marsha.staging.foo.com (considering that the
domain name is foo.com).

> Note that the route we are pointing to **should exist** and target an existing
> service declared in your project.

You can add this configuration at any time of your project's life. Once added,
you will need to create (or update) the redirection application and routes _via_
the `create_redirect.yml` playbook:

```bash
$ bin/ansible-playbook create_redirect.yml -e "env_type=staging customer=eugene"
```

> Please note that Arnold will issue an SSL certificate for each created route
> (_i.e._ redirection). Hence, you must be aware of [let's encrypt
> quota](https://letsencrypt.org/docs/rate-limits/) for your domain to avoid
> reaching that limit and not being able to issue SSL certificates for a
> redirection.
