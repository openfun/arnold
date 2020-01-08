# Upgrade

All instructions to  upgrade this project from  one release to the  next will be
documented in this  file. Upgrades must be run sequentially,  meaning you should
not skip minor/major releases while upgrading (fix releases can be skipped).

The format is inspired from [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## Unreleased

### Static services

This version introduces `Static services` and it is a breaking change in the
blue/green deployment process. The `switch` playbook is patching static services
instead of routes. And the `deployment_stamp` of the deployed stacks is no
longer stored in routes, but in static services instead.

In order to migrate to this new system, you have to apply the following upgrade
process. This will not cause any downtime, but it implies a redeployment of your
applications.

#### Upgrade Procedure

This procedure must be applied for every arnold application deployed.

The `current` stack of your application (before applying this procedure) will be
referred to as `BEFORE-UPGRADE-VERSION`.


##### 1. Upgrade your arnold version

##### 2. Execute the `create_services` ansible playbook :

```
bin/ansible-playbook create_services.yml -e "apps_filter=your-application"
```
It will create the static services required by your application. Each variant of these static services (`previous`, `current`, `next`) will target nothing after this step.

##### 3. Execute the `deploy` ansible playbook :

```
bin/deploy -e "apps_filter=your-application"
```

It will deploy your application and the `next` static services will target this
stack.

This step does not affect routes. So your `BEFORE-UPGRADE-VERSION` stays
unchanged and available via the `current` route. On the other hand, the `next`
stack you just deployed will not be reachable by any route.

##### 4. Execute the `switch` ansible playbook :

```
bin/switch -e "apps_filter=your-application"
```

The switch will be done at the static services level. So, the stack you just
deployed will be considered as the `current` by static services and by the
ansible playbooks.

But again, this step does not affect routes. So your `BEFORE-UPGRADE-VERSION`
stack stays unchanged and available via the `current` route.

##### 5. Execute the `create_routes` playbook :

```
bin/ansible-playbook create_routes.yml -e "apps_filter=your-application"
```

This will patch the routes to target the corresponding static services. After
this step, your `BEFORE-UPGRADE-VERSION` will be unavailable and will be
replaced by the `current` stack you just deployed.


##### 6.  Check and clean

Check that  everything is  OK  and execute  the `clean`  playbook to  remove
unreferenced stacks :

```
bin/clean -e "apps_filter=your-application"
```
