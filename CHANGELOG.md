# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic
Versioning](http://semver.org/spec/v2.0.0.html).

## Unreleased

## [6.7.0] - 2021-11-26

### Added

- `resume` and `pause` CLI commands now have an optional `SELECTOR` argument to
  target specific resources using k8s label selector requests; the `-a <APP>`
  arnold command flag is also supported

### Changed

- Upgrade `ansible` to `4.8.0`

### Removed

- Marsha: remove check_live_idle cronjob

## [6.6.0] - 2021-10-28

### Added

- ashley: create custom settings module
- ashley: allow to set unlimited secrets

### Changed

- Upgrade `ansible` to `4.7.0`

## [6.5.2] - 2021-10-21

### Fixed

- Fix subpath-based trays upgrade

## [6.5.1] - 2021-10-19

### Fixed

- Allow declaring alternative routes for Ashley as a workaround to third party
  cookies being blocked by some browsers

## [6.5.0] - 2021-10-14

### Added

- Community applications (_i.e._ trays not distributed with Arnold) can now be
  fetched, installed, configured & deployed.

## [6.4.0] - 2021-09-29

### Added

- Implemented support for RBAC objects

### Changed

- Upgrade `ansible` to `4.6.0`
- Upgrade to python 3.9

## [6.3.0] - 2021-09-16

### Added

- Prosody: enable mod_smacks when websocket is enabled
- Prosody: allow to configure nginx proxy read and send timeout

## [6.2.0] - 2021-09-14

### Added

- Marsha: cronjob running clean_medialive_dev_stack management command

## [6.1.0] - 2021-08-24

### Added

- Marsha: cronjob running clean_mediapackages management command

## [6.0.0] - 2021-08-11

### Added

- Allow deactivating `acme` ingress annotation for some blue/green prefixes
- CLI: add `acme` command to create or update the namespace TLS certificate
  Issuer
- Elasticsearch: add support for persistent volume to store indexes data
- Prosody: create new application for this XMPP server

### Changed

- Update `hello` app to be compatible with k8s
- Replace DeploymentConfig with Deployment in Ansible core tasks
- Replace Route with Ingress in Ansible core tasks
- Use `cert-manager` instead of `openshift-acme` for TLS certificates
  generation
- Use `kubectl` instead of `oc` in `arnold` CLI
- Authentication in `arnold` CLI must be done with a service account
- Replace `oc cluster` with k3d for local development
- CLI: autodetect if we are within a terminal
- Update Kibana user name to `kibana_system` for recent releases compatibility
- Removed python dependency for Kibana probes

### Fixed

- CLI: fix the `No such file or directory` error in the `vaults` command

### Removed

- Remove deprecated moodlenet and learninglocker apps that won't be upgraded
  to k8s
- Remove `acme` annotation from flower app ingress as it should not be
  accessible

## [5.25.0] - 2021-03-05

### Added

- Marsha: cronjob running check_harvested management command
- Marsha: cronjob running check_live_idle management command

### Removed

- Nextcloud: remove usage of BuildConfig and ImageStream objects
- Build image and image stream playbooks
- Marsha: remove collectstatic job

## [5.24.0] - 2021-01-19

### Changed

- CLI: mount local `env_type` directory if it exists
- CLI: the new `--extra-volume` option allows to mount an extra volume in the
  arnold container
- CLI: implement `--k8s-domain` option support

### Fixed

- Fix typos in setting names: `withelist` vs `whitelist` (BC)
- Fix apps management when only a single app is available

## [5.23.0] - 2021-01-05

### Added

- Add `arnold` CLI

## [5.22.1] - 2020-12-10

### Changed

- nextcloud tests have been removed from requirements to publish the arnold
  docker image with CircleCI

## [5.22.0] - 2020-12-08

### Added

- Add support for ashley 1.0.0-beta.3

### Fixed

- Fix memory lock configuration for elasticsearch 5.x

## [5.21.3] - 2020-11-19

### Fixed

- Fix Docker lint error by passing --no-cache-dir option on pip install
- Allow authenticating to pull images everywhere it is missing

### Removed

- Forum app build config and directly use image from external registry

## [5.21.2] - 2020-11-18

## Fixed

- Set Referer header with Origin header when empty in edxapp's lms nginx

## [5.21.1] - 2020-11-10

### Removed

- Obsolete "memcached" service from edxapp app (cache now runs on Redis)

## [5.21.0] - 2020-11-06

### Added

- new variable `acme_enabled_route_prefix` allowing to activate acme
  based on route prefix
- cronjob in Marsha to stop live streaming still living and unused

### Fixed

- Add missing FRONTEND_BASE_URL variable in moodlenet
- Fix moodlenet-pvc-uploads PVC declaration in moodlenet
- Fix basic auth in moodlenet nginx configuration
- Move moodlenet email credentials to vault and secret files
- Add missing location in moodlnet nginx configuration

## [5.20.0] - 2020-11-05

### Added

- Add `moodlenet` application

### Fixed

- Move `acme` ConfigMap annotation type to string

## [5.19.0] - 2020-10-21

### Added

- Allow extending ElasticSearch configuration template

### Fixed

- YAML syntax errors in ES job template

## [5.18.0] - 2020-10-16

### Added

- Allow extending kibana configuration template

## [5.17.0] - 2020-10-09

### Added

- Allow to change PVC media name

## [5.16.0] - 2020-09-30

### Added

- Allow extending nginx configuration templates on all sites

## [5.15.0] - 2020-09-22

### Changed

- Upgrade `ansible` to `2.9.13`
- Upgrade `edxapp` version to `ironwood.2-1.0.1`

## [5.14.2] - 2020-09-03

### Fixed

- Fix the `delete_app` task to avoid timeout errors during a `clean`

## [5.14.1] - 2020-08-31

### Fixed

- Pin transifex-client version in edx i18n job

## [5.14.0] - 2020-08-21

### Added

- Add CORS headers for richie static files to allow placing them behind a CDN

### Changed

- Inject configmap env in all jobs to allow defining settings that are required
- Upgrade `ansible` to `2.9.12`
- Create only required `openshift-acme` CM given the project environment

## [5.13.1] - 2020-07-23

### Fixed

- Exclude `openshift-acme` routes when looking for app routes

## [5.13.0] - 2020-07-22

### Added

- Implement support for Elasticsearch cluster secure mode
- Implement support for Kibana secure mode

### Changed

- Upgrade `openshift` to `0.11.2`
- Upgrade `ansible` to `2.9.10`

## [5.12.0] - 2020-06-09

### Fixed

- Recent `openshift-acme` releases require more permissions in the current
  namespace

### Removed

- Use new custom nginx image in the richie app allows to remove the
  collectstatic job and the static files volume

## [5.11.1] - 2020-05-27

### Fixed

- NGINX default configuration were broken when using whitelisted IP condition
- Remove unused `kibana_nginx_admin_ip_withelist` variable

## [5.11.0] - 2020-05-27

### Added

- New `kibana` application
- ElasticSearch `7.0+` releases are now supported
- Implemented `StatefulSet` k8s objects support

### Changed

- Upgrade `openshift` to `0.11.1`
- Upgrade `ansible` to `2.9.9`
- Upgrade `jmespath` to `0.10.0`

## [5.10.0] - 2020-05-19

### Changed

- Upgrade `yq` to `2.10.1`

### Removed

- Remove now useless static volume and collecstatic jobs from edxapp
- Remove build configurations and image streams from edxapp and rely on
  images built externally and embedding their theme and static files

## [5.9.0] - 2020-05-11

### Added

- Allow to set unlimited secrets in Marsha
- Create custom settings module in Marsha

### Changed

- Allow to disable persistence in redis-sentinel

## [5.8.0] - 2020-04-28

### Changed

- Split API and XAPI requests in marsha

## [5.7.0] - 2020-04-23

### Added

- Implemented support for generic ConfigMap templates

### Changed

- Upgrade `ansible` to `2.9.7`

## [5.6.0] - 2020-04-20

### Changed

- Upgrade `openshift` to `0.11.0`
- Use lightship-based health checks for the `etherpad` application (requires a
  recent `fundocker/etherpad` docker image; at least `1.8.0-education-1.2.0`).

### Fixed

- Improve pm2 logs configuration for the `learninglocker` application

## [5.5.0] - 2020-04-09

## Added

- New `etherpad` application

## Changed

- Update `nextcloud` app scripts path to: `/usr/local/bin`

## Fixed

- Create `.ocdata` file in the `data` directory for the Nextcloud image
- Restore `edxapp` custom theme support (front-end translations in `nginx`
  collectstatic BC)
- Use nextcloud image built by our BC in the Nginx InitContainer

## [5.4.0] - 2020-04-03

### Added

- New `nextcloud` application
- Add nginx status endpoint in `ashley`, `edxapp`, `edxec`, `flower`,
  `learninglocker`, `marsha`, `nextcloud` and `richie`.

### Changed

- Run learninglocker using pm2 process manager

## [5.3.0] - 2020-03-31

### Added

- New `ashley` application

### Changed

- Upgrade PyYAML to `5.3.1`
- Upgrade `acme` core app to its latest release that supports ACME v2 API

### Removed

- Stop declaring a specific tag for the `edxapp-nginx` docker image and use
  the `edxapp` image tag for both the `edxapp` and `nginx` images

### Fixed

- Temporarily reinstate the static volume on edxapp pods to allow using the
  `nginx` docker image with bundled static files, while waiting for a
  long-term fix

## [5.2.0] - 2020-03-23

### Changed

- Upgrade Ansible to `2.9.6`
- Upgrade `openshift` to `0.10.3`

### Fixed

- Fix syntax error in elasticsearch configuration file
- Configure the `redis` container to listen to all network interfaces

## [5.1.0] - 2020-02-27

### Added

- Add argument to `ci-test-route` to configure the maximum number of retries

### Changed

- Upgrade ansible to `2.9.5`

### Fixed

- `elasticsearch-discovery` service is not a headless service anymore
- Generate a valid YAML value from `elasticsearch_memory_lock` variable
- Set `edxapp`'s jobs image pull policy to "Always"
- Force creation of `/edx/app/edxapp/staticfiles` directory in `bc_nginx` build config

## [5.0.0] - 2020-01-31

### Added

- New application `elasticsearch` deployable _via_ Arnold
- Configured nginx cache for statics and media files for the following apps:
  - `richie`
  - `marsha`
  - `edxec`
  - `edxapp`
- Bypass htaccess using a whitelist ip for the following apps:
  - `richie`
  - `marsha`
  - `edxec`
  - `edxapp`
- Handle `CronJob` object type
- Introduce static services to expose services to other apps with a fixed name
- Add a static service for the elasticsearch forum

### Changed

- `edxapp`'s `nginx` service now uses a docker image with bundled CMS & LMS
  static files (even for custom themes)
- Upgrade `ansible` to 2.9.4
- Upgrade `openshift` to 0.10.1

### Fixed

- Error while generating JSON config file from jinja2 template

### Removed

- `edxapp`'s static files collection jobs are no longer required
- `edxapp`'s static files PV is no longer required

## [4.7.0] - 2020-01-17

### Added

- Create `flower` application

### Changed

- Use the `k8s_info` module instead of the deprecated `k8s_facts` module
- Prevent switching if next stack is not deployed

### Fixed

- Avoid downtime during a switch or rollback
- Improve `delete_previous` playbook behavior on k8s api failure
- Remove deprecation warnings in playbooks

## [4.6.0] - 2020-01-13

### Added

- Job in edxapp to create required directories in volumes
- Whitelist ips authorized to access /admin on edxapp,
  edxec, marsha and richie
- Whitelist ips authorized to access learninglocker's UI

### Fixed

- In edxapp, add an lms queue to the list of cms Celery queues
- Add edxec to eugene/development apps list

## [4.5.0] - 2020-01-08

### Added

- Make OpenEdx E-Commerce application (_aka_ `edxec`) deployable _via_ Arnold

## [4.4.0] - 2020-01-08

### Added

- Configure routing timeout in edxapp application

### Changed

- Update README.md about the oc version to use

### Fixed

- Update eugene/development vault file for learninglocker
- Fix MONGODB_HOST for eugene/development environment
- Fix local ip address detection in dev script

## [4.3.1] - 2019-12-23

### Changed

- Upgrade the learninglocker image to v5.2.2 and the xapi-service image to v2.9.10
- Set MongoDB 4.0 as the default database version for the learninglocker app

### Fixed

- Fix npm installation in Eucalyptus flavors
- The forum API key generated a syntax error when its last character was a ":"

### Added

- Add resources requests to all applications to improve pod scheduling.

## [4.3.0] - 2019-12-13

### Added

- Define mongo ips at the application level

## [4.2.0] - 2019-12-10

### Changed

- Apply PodAntiAffinity rules to redis-sentinel app

### Fixed

- Use the `forum_elasticsearch_host` variable in the forum application to make
  it overridable

## [4.1.2] - 2019-12-10

### Fixed

- Checking the number of running pods was hanging when redeploying an already
  running `redis-sentinel` app.

## [4.1.1] - 2019-12-09

### Fixed

- Inject XAPI secret as environment variable in XAPI DeploymentConfig

## [4.1.0] - 2019-12-06

### Added

- Create a new app redis-sentinel. This app uses the redis-operator
  (https://github.com/spotahome/redis-operator) and it must be installed
  on your OpenShift cluster before deploying.

### Removed

- Probes on edxapp workers. Existing probes are not compatible with redis sentinel.
  To use them with redis sentinel, we must use a Django management command or Celery
  using Django settings, but doing so is too slow to be considered as a relevant alternative.
  This removal is temporary, a new solution will be developped soon.

## [4.0.0] - 2019-11-26

### Added

- Configure MongoDB to use replicaSet and read_preference settings for all
  applications working with MongoDB

## [3.3.1] - 2019-11-25

### Fixed

- Fix syntax error in richie app templates following change in indentation

## [3.3.0] - 2019-11-25

### Added

- Allow deactivating volumes for static and media files in the richie app

### Changed

- Upgrade Ansible to `2.9.0`
- Upgrade OpenShift to `0.10.0`
- Upgrade `yq` to `2.8.1`
- Create a config map to manage redis configuration

### Fixed

- Set sentry in marsha secret only if present in the vault
- Ignore creating empty volume templates

## [3.2.0] - 2019-10-25

### Changed

- Upgrade Ansible to `2.8.6`
- Generate `edxapp` theme translations in target image build configuration

### Fixed

- Fixed broken `edxapp` jobs container image name when enabling a custom theme

## [3.1.1] - 2019-10-09

### Fixed

- Task that creates a secret with credentials for private Docker registries.

## [3.1.0] - 2019-10-07

### Added

- Implement support for docker private registry secrets
- Make private docker registry usage available for richie
- Allow to configure HTTP Basic Auth protection on a per-app basis

## [3.0.1] - 2019-10-04

### Fixed

- Remove extra quotes from redis healthcheck commands

## [3.0.0] - 2019-10-03

### Changed

- Upgrade OpenShift to OpenShift `0.9.2`
- Upgrade Ansible to `2.8.5`
- Switch learning locker to blue/green stategy

## [2.8.0] - 2019-08-23

### Changed

- `redis` app heath check probes now check that the data volume is accessible
  with write permissions

### Security

- Upgrade Ansible to `2.7.12` (see
  [CVE-2019-10156](https://nvd.nist.gov/vuln/detail/CVE-2019-10156))

## [2.7.0] - 2019-07-18

### Added

- The `build_images` playbook is now synchronous, waiting for target
  ImageStreamTags to be created

### Changed

- `edxapp` BuildConfig names now include the theme tag (if any) to avoid having
  to force their creation
- We now remove pods prior to other linked objects to avoid application issues
  with pods losing database connection or mounted ConfigMap volume

## [2.6.0] - 2019-07-15

### Changed

- Upgrade OpenShift to OpenShift `0.9.0`
- Use Celery native commands instead of Django management commands in celery
  worker probes

## [2.5.1] - 2019-06-24

### Fixed

- Ignore expected secrets checking for logged users with no permission on
  secrets

## [2.5.0] - 2019-06-21

### Added

- Ensure expected secrets exists before deploying an application
- Add `delete_previous.yml` playbook to delete previous stacks (should be used
  with caution)
- Add a `rollback.yml` playbook to restore the previous stack as the current one
- Add a `clean.yml` playbook to remove orphan stacks (not associated to any
  route) for blue-green-compatible applications

### Changed

- Optimize `edxapp` workers liveness probe frequency and replication to lower
  base cluster load

## [2.4.2] - 2019-06-12

### Changed

- Upgrade `openshift` to `0.8.9`
- Increase pods liveness/readiness probes periodicity to smooth pods replacement
  scheduling

## [2.4.1] - 2019-06-04

### Fixed

- Rename `edxapp` `nginx` service configuration location from `export` to
  `restricted`
- Configure `Richie` `SILENCED_SYSTEM_CHECKS` setting to allow `X_FRAME_OPTIONS`
  value set as `SAMEORIGIN`

## [2.4.0] - 2019-05-28

### Added

- Add an environment file to Richie application

### Changed

- Increase length of secret keys to 50 characters
- Mount the edxapp `export` volume in its nginx service and modify the nginx
  configuration to serve the files in this folder via X-Accel
- Rename the edxapp `exports` volume to `export`

## [2.3.0] - 2019-05-23

### Added

- Richie's bootstrapping requires to set up base pages tree _via_ the
  `richie_init` Django management command; this is performed thanks to a new job
  in the `richie` app

## [2.2.0] - 2019-05-21

### Added

- Add an environment file to Marsha application

### Changed

- Marsha volumes are used only in trashable environments

## [2.1.0] - 2019-05-10

### Changed

- Richie's application templates are now more generic to easily configure and
  deploy a custom instance

## [2.0.0] - 2019-05-07

### Added

- We now perform health checks to every service pods by implementing and
  defining `livenessProbe` and `readinessProbe` (except for Learninglocker
  applications).
- The `merge_with_app` filter now allows to override templates for a namespace
  (_e.g._ for an application/service) based on its file name.

### Changed

- Upgrade `openshift` to `0.8.8`
- Migrate apps to the new tray package tree (BC)
- Refactor and test the `apps` lookup to support the new tray package tree (BC)

### Fixed

- The project display name is no longer empty when creating a new project

## [1.10.0] - 2019-04-24

### Added

- Add `jq` and `yq` utilities to the Docker image

### Changed

- Rename the `ES_CLIENT` setting to `RICHIE_ES_HOST` for compatibility with
  Richie starting from version v1.0.0-beta.6.

### Removed

- Richie and Marsha applications no longer use dedicated `ImageStream` and
  `BuildConfig`

## [1.9.0] - 2019-04-11

### Added

- Add new volume to `edxapp` to store CSV reports

### Changed

- Upgrade Ansible to the 2.7.10 release

### Fixed

- Flag `collectstatic` jobs as "pre" jobs for all Django apps to prevent cache
  bursting issues

## [1.8.3] - 2019-04-03

### Fixed

- Fix Richie deployments by mounting the `media` volume in the
  `bootstrap_elasticsearch` job

## [1.8.2] - 2019-04-02

### Fixed

- Frontend translations are now properly updated while deploying `edxapp`
- The bin/job was broken due to recent changes in the `_docker_run` usage

## [1.8.1] - 2019-04-02

### Fixed

- fix DJANGO_CLOUDFRONT_DOMAIN variable in marsha secret template

## [1.8.0] - 2019-04-01

### Added

- Configure PyUp to submit dependency updates every week
- Add DJANGO_AWS_S3_REGION_NAME in marsha secret configuration
- Add DJANGO_CLOUDFRONT_DOMAIN in marsha secret configuration

### Fixed

- Add missing location to serve media files in the `nginx` configuration of the
  Richie app.

## [1.7.0] - 2019-03-22

### Added

- Richie's app BuildConfig now supports extra dependencies installation

### Changed

- Python dependencies have been upgraded thanks to pyup bot.
- `pip` requirements file has been moved to `requirements.txt` at the project's
  root
- Supplementary `ansible-lint` rules are now provided by the
  [lean-delivery/ansible-lint-rules](https://github.com/lean-delivery/ansible-lint-rules)
  maintained project
- Marsha and richie BuildConfig force to pull the latest available docker image
- CircleCI docker cache has been inactivated to prevent job failures from cache
  issues
- Ansible vaults password is now required only when needed, _i.e._ when creating
  secrets (_e.g._ when using the `init_project` or `bootstrap` playbooks)

### Security

- Upgrade PyYAML to 5.1 (see https://nvd.nist.gov/vuln/detail/CVE-2017-18342)

## [1.6.0] - 2019-03-18

### Added

- Create a volume for learning locker. This volume will be mounted in the
  storage repository

### Changed

- Upgrade Richie to the `master` docker image by default

## [1.5.1] - 2019-02-27

### Added

- Make local docker image build closest to CI conditions
- Ignore all customers except eugene in local docker image builds

### Removed

- Obsolete GitLab CI configuration

## Fixed

- Improve DC pods selectors in DC deployment wait loop
- Fix "jobs" variable collision during jobs submission

## [1.5.0] - 2019-02-20

### Added

- Upgrade Ansible to version 2.7.7
- Upgrade OpenShift to version 0.8.4
- Switch from the `openshift_raw` to the `k8s` module
- Use the `k8s_facts` module instead of the `k8s` lookup
- Make our `docker run` wrapper rock-solid
- Refactor CI tools to have only one script: `bin/ci-ansible-playbook`
- Refactor and test `delete_app` tasks in the CI

### Fixed

- Fix broken `edxapp`'s MySQL pod secrets due to a recent update in the `latest`
  image.

## [1.4.0] - 2019-02-11

### Added

- Publish a Docker image to DockerHub for the master branch
- The `apps_filter` variable definition is now required to run the `switch.yml`
  and `deploy.yml` playbooks (if multiple apps are active)
- Upgrade Richie to its latest release (`1.0.0-beta.1`)
- Upgrade default `edxapp` image to `hawthorn.1-2.6.0`
- Add default `memcached` configuration for `edxapp`

## [1.3.0] - 2019-01-31

### Added

- Add support for LRS variables in Marsha.

## [1.2.0] - 2019-01-28

### Added

- Migrate docker image to python 3.6

## [1.1.0] - 2019-01-25

### Added

- Create ConfigMaps to be consumed in environment variables in a
  DeploymentConfig.
- Add learning locker in the list of supported applications.
- Activate and configure learning locker for the eugene customer in development
  & CI environments.
- ConfigMap generation is now compatible with non-blue-green core applications.
- The redirect application is now part of Arnold's core features, with it's own
  life cycle.

## [1.0.0] - 2019-01-22

### Added

- Allow to force route substitution (delete & create) using the force_route
  variable.

### Fixed

- The redirect application deployment was failing due to a side effect in route
  objects creation refactoring (#233).

## [1.0.0-alpha.8] - 2019-01-21

### Added

- Allow to define multiple Service objects.
- Make the `init_project` playbook composable by externalizing some tasks in two
  new playbooks: `create_routes` and `create_image_streams`.

## [1.0.0-alpha.7] - 2019-01-17

### Added

- Add a new check in the CI to ensure that the CHANGELOG has been modified in a
  submitted pull request.
- Add support for extra dependencies installation in edxapp Docker image that
  will be deployed.

## [1.0.0-alpha.6] - 2019-01-09

### Added

- Add a new create_volumes playbook to create volumes on an existing project

### Fixed

- Add app namespace in front of the DJANGO_CLOUDFRONT_PRIVATE_KEY variable where
  missing

## [1.0.0-alpha.5] - 2019-01-04

### Added

- Allow configuring several replicas for stateless applications and nginx pods
- Spread replicas on all OpenShift nodes for optimal redundancy
- Don't rely on cookies to route requests but use round robin assignment

### Fixed

- Rename edxapp celery worker pods for coherence with wsgi pods
- Remove use of deprecated assertEquals that were breaking CI tests

## [1.0.0-alpha.4] - 2018-12-21

### Added

- Implement support for pre and post-deployment jobs
- Add internationalization job to fetch latest translations update

### Fixed

- Edxapp Celery workers DC names are now more explicit (worker vs wsgi)
- Edxapp internationalization-related objects are now properly created

## [1.0.0-alpha.3] - 2018-12-19

### Added

- Edxapp Celery workers are now configurable (number of replicas and queues to
  consume) (#207)

### Fixed

- Pods deployment wait loop is now more robust by relying on the number of pod
  replicas instead of the number of deployments (#207)
- Add missing ask-vault-pass option in bin/built_images script (#210)
- Prevent htpasswd file overriding when running the create htpasswd playbook
  multiple times (#211)

## [1.0.0-alpha.2] - 2018-12-14

### Added

- Studio preview route for edxapp
- Validation pre-task (check environment name)

### Fixed

- Namespace application vault variables to avoid cross-application collisions
- Add missing optional EDXAPP_THEME_GIT_PRIVATE_KEY variable in edxapp vault
  template

## [1.0.0-alpha.1] - 2018-12-10

### Added

- First Arnold's public release
- Official Docker image is available at:
  https://hub.docker.com/r/fundocker/arnold/

[unreleased]: https://github.com/openfun/arnold/compare/v6.7.0...master
[6.7.0]: https://github.com/openfun/arnold/compare/v6.6.0...v6.7.0
[6.6.0]: https://github.com/openfun/arnold/compare/v6.5.2...v6.6.0
[6.5.2]: https://github.com/openfun/arnold/compare/v6.5.1...v6.5.2
[6.5.1]: https://github.com/openfun/arnold/compare/v6.5.0...v6.5.1
[6.5.0]: https://github.com/openfun/arnold/compare/v6.4.0...v6.5.0
[6.4.0]: https://github.com/openfun/arnold/compare/v6.3.0...v6.4.0
[6.3.0]: https://github.com/openfun/arnold/compare/v6.2.0...v6.3.0
[6.2.0]: https://github.com/openfun/arnold/compare/v6.1.0...v6.2.0
[6.1.0]: https://github.com/openfun/arnold/compare/v6.0.0...v6.1.0
[6.0.0]: https://github.com/openfun/arnold/compare/v5.25.0...v6.0.0
[5.25.0]: https://github.com/openfun/arnold/compare/v5.24.0...v5.25.0
[5.24.0]: https://github.com/openfun/arnold/compare/v5.23.0...v5.24.0
[5.23.0]: https://github.com/openfun/arnold/compare/v5.22.1...v5.23.0
[5.22.1]: https://github.com/openfun/arnold/compare/v5.22.0...v5.22.1
[5.22.0]: https://github.com/openfun/arnold/compare/v5.21.3...v5.22.0
[5.21.3]: https://github.com/openfun/arnold/compare/v5.21.2...v5.21.3
[5.21.2]: https://github.com/openfun/arnold/compare/v5.21.1...v5.21.2
[5.21.1]: https://github.com/openfun/arnold/compare/v5.21.0...v5.21.1
[5.21.0]: https://github.com/openfun/arnold/compare/v5.20.0...v5.21.0
[5.20.0]: https://github.com/openfun/arnold/compare/v5.19.0...v5.20.0
[5.19.0]: https://github.com/openfun/arnold/compare/v5.18.0...v5.19.0
[5.18.0]: https://github.com/openfun/arnold/compare/v5.17.0...v5.18.0
[5.17.0]: https://github.com/openfun/arnold/compare/v5.16.0...v5.17.0
[5.16.0]: https://github.com/openfun/arnold/compare/v5.15.0...v5.16.0
[5.15.0]: https://github.com/openfun/arnold/compare/v5.14.2...v5.15.0
[5.14.2]: https://github.com/openfun/arnold/compare/v5.14.1...v5.14.2
[5.14.1]: https://github.com/openfun/arnold/compare/v5.14.0...v5.14.1
[5.14.0]: https://github.com/openfun/arnold/compare/v5.13.1...v5.14.0
[5.13.1]: https://github.com/openfun/arnold/compare/v5.13.0...v5.13.1
[5.13.0]: https://github.com/openfun/arnold/compare/v5.12.0...v5.13.0
[5.12.0]: https://github.com/openfun/arnold/compare/v5.11.1...v5.12.0
[5.11.1]: https://github.com/openfun/arnold/compare/v5.11.0...v5.11.1
[5.11.0]: https://github.com/openfun/arnold/compare/v5.10.0...v5.11.0
[5.10.0]: https://github.com/openfun/arnold/compare/v5.9.0...v5.10.0
[5.9.0]: https://github.com/openfun/arnold/compare/v5.8.0...v5.9.0
[5.8.0]: https://github.com/openfun/arnold/compare/v5.7.0...v5.8.0
[5.7.0]: https://github.com/openfun/arnold/compare/v5.6.0...v5.7.0
[5.6.0]: https://github.com/openfun/arnold/compare/v5.5.0...v5.6.0
[5.5.0]: https://github.com/openfun/arnold/compare/v5.4.0...v5.5.0
[5.4.0]: https://github.com/openfun/arnold/compare/v5.3.0...v5.4.0
[5.3.0]: https://github.com/openfun/arnold/compare/v5.2.0...v5.3.0
[5.2.0]: https://github.com/openfun/arnold/compare/v5.1.0...v5.2.0
[5.1.0]: https://github.com/openfun/arnold/compare/v5.0.0...v5.1.0
[5.0.0]: https://github.com/openfun/arnold/compare/v4.7.0...v5.0.0
[4.7.0]: https://github.com/openfun/arnold/compare/v4.6.0...v4.7.0
[4.6.0]: https://github.com/openfun/arnold/compare/v4.5.0...v4.6.0
[4.5.0]: https://github.com/openfun/arnold/compare/v4.4.0...v4.5.0
[4.4.0]: https://github.com/openfun/arnold/compare/v4.3.1...v4.4.0
[4.3.1]: https://github.com/openfun/arnold/compare/v4.3.0...v4.3.1
[4.3.0]: https://github.com/openfun/arnold/compare/v4.2.0...v4.3.0
[4.2.0]: https://github.com/openfun/arnold/compare/v4.1.2...v4.2.0
[4.1.2]: https://github.com/openfun/arnold/compare/v4.1.1...v4.1.2
[4.1.1]: https://github.com/openfun/arnold/compare/v4.1.0...v4.1.1
[4.1.0]: https://github.com/openfun/arnold/compare/v4.0.0...v4.1.0
[4.0.0]: https://github.com/openfun/arnold/compare/v3.3.1...v4.0.0
[3.3.1]: https://github.com/openfun/arnold/compare/v3.3.0...v3.3.1
[3.3.0]: https://github.com/openfun/arnold/compare/v3.2.0...v3.3.0
[3.2.0]: https://github.com/openfun/arnold/compare/v3.1.1...v3.2.0
[3.1.1]: https://github.com/openfun/arnold/compare/v3.1.0...v3.1.1
[3.1.0]: https://github.com/openfun/arnold/compare/v3.0.1...v3.1.0
[3.0.1]: https://github.com/openfun/arnold/compare/v3.0.0...v3.0.1
[3.0.0]: https://github.com/openfun/arnold/compare/v2.8.0...v3.0.0
[2.8.0]: https://github.com/openfun/arnold/compare/v2.7.0...v2.8.0
[2.7.0]: https://github.com/openfun/arnold/compare/v2.6.0...v2.7.0
[2.6.0]: https://github.com/openfun/arnold/compare/v2.5.1...v2.6.0
[2.5.1]: https://github.com/openfun/arnold/compare/v2.5.0...v2.5.1
[2.5.0]: https://github.com/openfun/arnold/compare/v2.4.2...v2.5.0
[2.4.2]: https://github.com/openfun/arnold/compare/v2.4.1...v2.4.2
[2.4.1]: https://github.com/openfun/arnold/compare/v2.4.0...v2.4.1
[2.4.0]: https://github.com/openfun/arnold/compare/v2.3.0...v2.4.0
[2.3.0]: https://github.com/openfun/arnold/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/openfun/arnold/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/openfun/arnold/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/openfun/arnold/compare/v1.10.0...v2.0.0
[1.10.0]: https://github.com/openfun/arnold/compare/v1.9.0...v1.10.0
[1.9.0]: https://github.com/openfun/arnold/compare/v1.8.3...v1.9.0
[1.8.3]: https://github.com/openfun/arnold/compare/v1.8.2...v1.8.3
[1.8.2]: https://github.com/openfun/arnold/compare/v1.8.1...v1.8.2
[1.8.1]: https://github.com/openfun/arnold/compare/v1.8.0...v1.8.1
[1.8.0]: https://github.com/openfun/arnold/compare/v1.7.0...v1.8.0
[1.7.0]: https://github.com/openfun/arnold/compare/v1.6.0...v1.7.0
[1.6.0]: https://github.com/openfun/arnold/compare/v1.5.1...v1.6.0
[1.5.1]: https://github.com/openfun/arnold/compare/v1.5.0...v1.5.1
[1.5.0]: https://github.com/openfun/arnold/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/openfun/arnold/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/openfun/arnold/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/openfun/arnold/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/openfun/arnold/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/openfun/arnold/compare/v1.0.0-alpha.8...v1.0.0
[1.0.0-alpha.8]: https://github.com/openfun/arnold/compare/v1.0.0-alpha.7...v1.0.0-alpha.8
[1.0.0-alpha.7]: https://github.com/openfun/arnold/compare/v1.0.0-alpha.6...v1.0.0-alpha.7
[1.0.0-alpha.6]: https://github.com/openfun/arnold/compare/v1.0.0-alpha.5...v1.0.0-alpha.6
[1.0.0-alpha.5]: https://github.com/openfun/arnold/compare/v1.0.0-alpha.4...v1.0.0-alpha.5
[1.0.0-alpha.4]: https://github.com/openfun/arnold/compare/v1.0.0-alpha.3...v1.0.0-alpha.4
[1.0.0-alpha.3]: https://github.com/openfun/arnold/compare/v1.0.0-alpha.2...v1.0.0-alpha.3
[1.0.0-alpha.2]: https://github.com/openfun/arnold/compare/v1.0.0-alpha.1...v1.0.0-alpha.2
[1.0.0-alpha.1]: https://github.com/openfun/arnold/compare/f9238a2...v1.0.0-alpha.1
