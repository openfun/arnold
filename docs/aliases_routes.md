# Aliases routes

The idea is that we would send all the traffic for a domain and it's subdomains
to OpenShift (HAproxy does not filter anymore). And we also want to redirect
some routes.

We then need to be able to:

- trigger redirects e.g (xyz.fr to www.xyz.fr)

## Method

To do this we deploy an Nginx service on port 8999. The Nginx configuration uses
a map to translate all redirected routes (aka aliases). All aliases routes are
linked to the Nginx service on the 8999 port.

## Usage

### Main URL

If your main routes are handled by OpenShift, then you must create an OpenShift
template in `templates/openshift/route`. And add them to the `openshift_routes`
variable.

### Aliases routes

#### Prerequisites

For each route you want to trigger, you must ensure that the DNS record points
to the OpenShift cluster.

#### Declare aliases

Each alias should be declared for a route in the `aliases` section of a route
(see the `group_vars/all/openshift_routes.yml` file).

For exemple, if you want to redirect `domain.tld` and `main-domain.tld` to
`www.maindomain.tld` then your route declaration may look like:

```yml
# OpenShift redirected_routes exemple
# openshift_aliases_routes:       # routes to be redirected
#   - route: www.maindomain.tld   # main domain this route must be existe
#     aliases:                    # aliases to create for redirection to the main route
#       - maindomain.tld
#       - main-domain.tld
#   - route: main_route
#     aliases:
#       - alias_1
#       - alias_2
openshift_aliases_routes:
  - route: www.maindomain.tld
    aliases:
      - maindomain.tld
      - main-domain.tld
```
