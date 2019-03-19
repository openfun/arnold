# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

- Create ConfigMaps to be consumed in environment variables in a DeploymentConfig.
- Add learning locker in the list of supported applications.
- Activate and configure learning locker for the eugene customer in development & CI environments.
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

- Add app namespace in front of the DJANGO_CLOUDFRONT_PRIVATE_KEY variable where missing

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
- Official Docker image is available at: https://hub.docker.com/r/fundocker/arnold/

[unreleased]: https://github.com/openfun/arnold/compare/v1.6.0...master
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
