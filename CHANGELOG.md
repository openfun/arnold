# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic
Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[unreleased]: https://github.com/openfun/arnold/compare/v4.1.2...master
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
[1.0.0-alpha.1]: https://github.com/openfun/arnold/compare/f9238a2...v1.0.0-alpha.1
