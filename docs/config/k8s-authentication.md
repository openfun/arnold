# Authenticating against Kubernetes

In this documentation, we'll see how to connect arnold to a remote Kubernetes
cluster.

## Service account

In order to deploy applications on a Kubernetes cluster, `arnold` needs to have
a `ServiceAccount` provided.

This service account requires to have enough permissions, including:
- The right to create and get namespaces
- The right to get, list, create, update, delete and patch all Kubernetes
  resources defined by arnold apps.

Since these resources depend on which arnold applications you will install, it
is hard to provide an exhaustive list of required permissions. That's why, we'll
show in the following example how to create a `ServiceAccount` with superuser
permissions. On a production cluster, you should not set superuser permissions
for `arnold` and handcraft permissions to your deployment needs.

We assume that you have a `kubectl` client configured to interact with your
Kubernetes cluster.

First, we create a `ServiceAccount` named `arnold` in the `default` namespace
with the following command :

```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: arnold
  namespace: default
EOF
```

And then, we create a `ClusterRoleBinding` to link the `arnold` ServiceAccount
to the `cluster-admin` ClusterRole. This role exists by default on Kubernetes
and has superuser permissions.

```bash
kubectl apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: arnold-cluster-admin
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: arnold
  namespace: default
EOF
```

That's it, you should now have an `arnold` Service Account in the `default`
namespace, with superuser permissions.

You can verify it with the following command:

```bash
kubectl -n default get serviceaccount arnold
```

Which should return:

```
NAME     SECRETS   AGE
arnold   1         1m
```

You can find more information about [Service Accounts](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/)
and [Authorizations](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
in the official [Kubernetes documentation](https://kubernetes.io/docs/).


## Providing credentials to arnold CLI


Now that we have a Service Account dedicated to arnold, we have to configure
arnold CLI to use it.

There are 2 ways to do this:

1. Using arnold's service account discovery mechanism
2. By providing the service account authentication token to arnold

The first method is the easiest. It is recommended if you use arnold from your
workstation. The second one is recommended for CI/CD environments.

### 1) Using arnold's service account discovery mechanism

Arnold CLI can discover the ServiceAccount authentication information based on
your local `kubectl` configuration. This method is recommended if you want to
use arnold CLI from your workstation.

The requirements to use this method are:
- having a `kubectl` CLI configured to connect to the Kubernetes cluster
- having sufficient permissions to read the ServiceAccount's secret


You have to provide the following environment variables to arnold CLI :

- `K8S_CONTEXT`
- `K8S_SERVICE_ACCOUNT`
- `K8S_SERVICE_ACCOUNT_NAMESPACE`


##### K8S_CONTEXT

The `K8S_CONTEXT` environment variable should contain the `context` name to use
to connect to your Kubernetes cluster.

This is necessary because the kubectl client can be configured to [connect to
multiple Kubernetes
clusters](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)
using contexts, and arnold CLI needs to know which context to use.

To list all contexts defined in your kubectl configuration, you can execute the
following command:

```bash
kubectl config get-contexts -o=name
```

To get the name of the current context used by your `kubectl` CLI, you can
execute the following command:

```bash
kubectl config current-context
```

For our example, we will consider that our context is named `my-k8s-cluster`.

##### K8S_SERVICE_ACCOUNT

The `K8S_SERVICE_ACCOUNT` environment variable should contain the ServiceAccount
name to use.

In our case, we created a ServiceAccount named `arnold` in the previous section.

##### K8S_SERVICE_ACCOUNT_NAMESPACE

The `K8S_SERVICE_ACCOUNT_NAMESPACE` environment variable should contain the name
of the namespace in which the ServiceAccount has been created.

In our case, we created a ServiceAccount in the `default` namespace.


To sum up, in our example, we need to provide the following environment
variables :

```bash
export K8S_CONTEXT=my-k8s-cluster
export K8S_SERVICE_ACCOUNT=arnold
export K8S_SERVICE_ACCOUNT_NAMESPACE=default
```

With these environment variables, arnold CLI will be able to connect to your
Kubernetes cluster, get the ServiceAccount authentication information and
provide them to the docker container that manages the deployment.

Note: If you encounter a TLS certificate error and your Kubernetes API
certificate is signed by a public trusted CA, you can set the following variable:

```bash
export USE_K8S_SERVICE_ACCOUNT_CA_CERT=0
```

### 2) Providing ServiceAccount authentication token

In some cases (like CI/CD environments), you don't have a `kubectl` CLI
configured to connect to your Kubernetes cluster and with sufficient permissions
to retrieve the ServiceAccount authentication information.

You must therefore provide the following environment variables to arnold CLI :

- `K8S_AUTH_API_KEY`: a service account authentication token
- `K8S_AUTH_HOST`: the k8s api host (e.g. `https://api.my-k8s-cluster.example/`)

To retrieve the service account authentication token, you can execute the
following command (assuming your ServiceAccount is named `arnold`, in the
`default` namespace):

```bash
SERVICE_ACCOUNT=arnold
SERVICE_ACCOUNT_NAMESPACE=default
kubectl -n "${SERVICE_ACCOUNT_NAMESPACE}" get secrets -o jsonpath="{.items[?(@.metadata.annotations['kubernetes\\.io/service-account\\.name']=='${SERVICE_ACCOUNT}')].data.token}"|base64 --decode
```
