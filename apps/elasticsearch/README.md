# Elasticsearch tray

## Secure the `elasticsearch` cluster

By default, similarly to the elastic-stack distribution, the `elasticsearch`
tray is deployed as "unsecured". This is perfectly fine for your test
environments or an internal usage. But, when you need to expose your cluster or
activate authentication backends (_e.g._ to access Kibana spaces),
`elasticsearch` requires that you activate the `xpack.security.enabled` mode.

Arnold's Elasticsearch tray fully automates the security mode configuration if
you set the `elasticsearch_security_enabled` ansible variable to `true` for
your customer or environment (extra variables can also be set to customize
paths and names for SSL certificates):

```yaml
# group_vars/eugene/staging/main.yml

elasticsearch_security_enabled: true

# Optional
elasticsearch_ssl_certificates_path: /path/to/certs
elasticsearch_ssl_certificates_name: foo.p12
```

### Generate your CA certificate and private key

To secure communication between nodes and between clients & the cluster, you
will need to generate SSL certificates derived from a CA certificate that
should be given as a secret in PEM format. To generate this certificate, we
will use the `elasticsearch-certutil` tool:

```
$ export ES_RELEASE=7.7.1
$ export ES_CA_PASSWORD="supersecret"
$ docker run --rm -t \
    docker.elastic.co/elasticsearch/elasticsearch:"${ES_RELEASE}" \
      bash -c " \
        elasticsearch-certutil ca -s --pem --out /tmp/ca.zip --pass \"${ES_CA_PASSWORD}\" && \
        unzip -p /tmp/ca.zip \
      "
```

> Note that your CA certicate is protected by a password that you also need to
> provide in a secret (more on this later).

### Edit project vault

Once generated, copy/paste your CA certificate in the project's Elasticsearch vault:

```yaml
# groups_vars/customer/eugene/staging/secrets/elasticsearch.vault.yml
CA_CERTIFICATE_PASSWORD: 'supersecret'
CA_CERTIFICATE: |
  -----BEGIN CERTIFICATE-----
  MIIDSTCCAjGgAwIBAgIUdgNCjjaLwtBCqDSP2gNbEV35N4cwDQYJKoZIhvcNAQEL
  BQAwNDEyMDAGA1UEAxMpRWxhc3RpYyBDZXJ0aWZpY2F0ZSBUb29sIEF1dG9nZW5l
  cmF0ZWQgQ0EwHhcNMjAwNjI2MDkyMDQxWhcNMjMwNjI2MDkyMDQxWjA0MTIwMAYD
  VQQDEylFbGFzdGljIENlcnRpZmljYXRlIFRvb2wgQXV0b2dlbmVyYXRlZCBDQTCC
  ASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALd2G/H7LLtQq6goPHk+Du6a
  ULGxu4cHiRIE0V+ZORvgNxBM/euiwOStgBMPrXrNDxaW7RAoHUimY9j8W/VgxY1i
  K7eFvDAF8p6Um9a/tIXrg5m6ro3pWsuCkk/bJt+KxjLFL+veHP36ehQUZG+MIMOg
  5fxt6WBZopRqk3HVsVgZonVO1r1o4oBPeabufjgLA3X9qCFc4NuLXPknvmKRbN+y
  SrZPKsdQGd/LMoEpR6pkhS/MUmeDTxJZciHo42Kb3ol1qFRAPZgESqC9XbWmdCo9
  1egayHpA7NaQIGgKVnLd0uROaGY7t0IJhfEIzSBlgrpQpeFp44y/e1I/g0KrLR0C
  AwEAAaNTMFEwHQYDVR0OBBYEFG8isTj98733+CDdTv2+yJbiv36PMB8GA1UdIwQY
  MBaAFG8isTj98733+CDdTv2+yJbiv36PMA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZI
  hvcNAQELBQADggEBABACIqzP+/zr/mVGlmuiwvT09/Ps6gY5F5TQW9OdqAtvE+5k
  hDYw6PnTxgXFQsTysGCOqhNmvTwhFiGZkwI2GhzqVCdnKPSNcYvR51RfTUR+mDnx
  TUvnws1eaJ97KFshUKBG9u2q16DT2DlfW588+9/iYl6JXxMkIZCP5Y2GOkfXhbtL
  VlH/nF9E8WCQKRy6eCyu4w5Ir14vTG+HvsIOyBCyGoPPhH47RO3e85s3NOpYRiEU
  X1zmR1hGlzX7GvIW8iFgIYbBOxdpffvx7KUlcI6SGT2ELEIuaQEaOnWb+j8VDfds
  EpRdxvGcL7N8UY7xdDRna7jXVYHnb8Ng15/GZC4=
  -----END CERTIFICATE-----
CA_PRIVATE_KEY: |
  -----BEGIN RSA PRIVATE KEY-----
  Proc-Type: 4,ENCRYPTED
  DEK-Info: AES-128-CBC,C6465BE14A3A13D711270EB1DE5EE8EC

  FerOdtzfkPLkef7F5A4ANagCMA7c9v9ivMj3rCpefpcfO7bwGp9NIczQwDO1mc6R
  2Na5VfgF5Ma5BMAQZFoU93Iai4aGMs6PU6fQNcPXkQMsm4Nij4d464qIwsLlE04F
  OPOFVmiNCOcYbG4EaSW8YTmQ4CQSLKxfMvbdReyxuaLgoTEprUEomu7aYK7bnsvM
  VhvP3fTb/FbQChu2mfkUvWwlBWGxSBau7dYwngIBpPsqzohPAMvTC7lyCbMDXrcB
  17oz+xRQIok3AAcdvZFXwP2yK4KI5DTSrVxQX+VJZzZuOOzW8LWs2U7yU0mYgtag
  Q7N8z15xOWzbmDVRqWdBq5BbMz7l5Ev/RYwGq61EGofma18O/q+eC7uqWn6A9BGf
  0lMVrSmylNz72lMa/k1v+Hs+JtcX3NQEsF04TlZbYQbjR9qh5M4PUxefmBKMjCRu
  NyalFJaK8hxG8+61xFKIVokRDdg8ABmre4/l42QlM4LLGhHAYMyJ/Hhi12dU88BI
  5K4vvbaMHrrzEn15l7slYn1jWkYn0iecmFUNjl8JVzUrU043wUlTijN33XOfJgAh
  O5clrBVVXTLigNUjDaZQIhYEwQyEtDTJ3+67vwqFKkNKlL52TVyB2vUNoq2Rn4+v
  9e2wtiOPKg7awu8eMieegJKrQM4bKklEQyRq3QgQtYXRNR6lDAFhE9cMdPJkZNqx
  cNWEXuk4Cxi9/siWgA5NmEsCBUltRhKIkSTrUsNVuUlw2TyzHVkBQbrDkY0zWt73
  4/5rYtJVQAQWANpIjE8MSLGNanQKX4sPN7Uf4zDjkdRLaEhfev1HFKRSDuWU1s4Z
  p5fRyeoiZ+vfNqMGilytVtbA5qtYN446YceIZ6CapTOlqkuGJZF9ZKKgoRPYtnHI
  UqZNiIQ+p+6usAPuS4BfrUIQ7wuqJwfoIad4J8LLtdsqCAoQ0VsBBgqzSWwGTc/m
  q9TB0lyiJs7aeUxqfCXkaM4Hbm70q0dq64ad2DLvvfvNOOfgN9d1exMVjEbbomx/
  DUpSvA84owE/PVi4/rojIY7FH2myv2GZ6uGTSmGcdpg2ZKTGsZwsMlc5T7l4tWxV
  NhRjQ87gkbzm37KFva0VB5eFzlqTd7+vMfrd+mYryfXEVJ9Lsmw/96ZPXV+Pwfb5
  AQ1HGpfiBL3LIICikNNJ8f0kSKfAdzyQjOx1fD093HyhN+i4BvSF9r2PWy4ajCwM
  /+Ko26QswEJJL42v9DJpsFsMJkUZdTgOQXnBoMjH3WVVp8xYIIKH+49Q3B8lGezd
  isTAXLQbU4o7LiYhEwr+EaZkvCKhLljRgsO9eKkE0JHkJqPsVRYpp22pnbjZO+pl
  5CDYmGwjAT39wESzvhcHrV5O/+ZuHP22skyfnpNXNRujj2WzoM+pMoiR88bfCrpF
  VLwclKKQiomeoKKMvyzDFdHH/SiytDG14utO8dn+67d8aai6AMCmHOKLmFoT/i0Y
  tSFlSmOQTfXgvAn3sWTrXYxRZgb+FDAS2LcWdyTFwLCMn60XksGED+GfCYM+Wi8l
  9aJkV26CRG8b1fG9XBKGH75u3dwrCsKnh3WjYLEHIPyLGPAUVnZ70iF5922rWm86
  -----END RSA PRIVATE KEY-----
```

### Create required objects

Now that your vault is up-to-date and encrypted, you will need to create
required secrets:

```
$ bin/ansible-playbook create_secrets.yml
```

and volumes:

```
$ bin/ansible-playbook create_volumes.yml
```

And voilà!
