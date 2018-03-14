# Arnold's

Arnold's is the place where all FUN's applications are assembled and deployed to Openshift as Docker micro services.

In order to deploy our applications, we need to generate configuration files customized for each project, being defined by the name of a site AND an environment:

- the site is a specific customer installation (**e.g.** fun, campus, corporate,...),
- each site is installed in several environments:
  * **feature:** one environment for each feature branch, the feature being described by its title (**e.g** feat/99-change-background-color),
  * **staging:** aggregating all features before a release,
  * **preprod:** validating a release before going live,
  * **production:** customer facing operations.

The deployment files are crafted by applying project variables to a set of Ansible templates.

To generate the deployment files, run:

    $ ansible-playbook deploy.yml -e "customer=corporate env_type=preprod"

The default env_type is `staging`.
The default customer is `patient0`, a demo site with default configuration.

For a `feature` environment, you should also set a `feature_title` variable with a slug describing the feature:

    $ ansible-playbook deploy.yml -e "env_type=feature feature_title=change-background-color"

The generated files should now be available in the `_result` directory.
