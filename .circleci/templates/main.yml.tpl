# CircleCI's configuration for Arnold
#
# Reference: https://circleci.com/docs/2.0/configuration-reference/

aliases:
  - &defaults
    docker:
      - image: circleci/python:3.6.5-stretch-node-browsers
    working_directory: ~/fun

  # Activate Docker in Docker (aka dind)
  - &dind
    setup_remote_docker:
      docker_layer_caching: false

  - &ci_env
    run:
      name: Define Environment Variable at Runtime
      command: |
        echo 'export ARNOLD_IMAGE="arnold:$(tr -d '\n' < VERSION)"' >> $BASH_ENV
        source $BASH_ENV

  - &docker_load
    run:
      name: Load docker image
      command: |
        docker load < /tmp/docker/images/arnold.tar
        docker images

  - &attach_workspace
    attach_workspace:
      # Must be absolute path or relative path from working_directory
      at: /tmp/docker

  - &install_openshift_cluster
    run:
      name: Install the OC client
      command: |
        wget https://github.com/openshift/origin/releases/download/v3.11.0/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz -P /tmp/openshift/
        tar xzf /tmp/openshift/openshift*.tar.gz --strip-components=1 -C /tmp/openshift/
        cp /tmp/openshift/oc $HOME/bin/

  - &configure_openshift_cluster
    run:
      name: Configure Docker for OpenShift cluster
      command: |
        # Elasticsearch requires to increase this setting's default value
        sudo sysctl -w vm/max_map_count=262144
        sudo bash -c "echo '{\"insecure-registries\": [\"172.30.0.0/16\"]}' > /etc/docker/daemon.json"
        sudo service docker restart

  - &run_openshift_cluster
    run:
      name: Run local OpenShift cluster & configure environment
      command: |
        export OPENSHIFT_DOMAIN=$(hostname -I | awk '{print $1}')
        export K8S_AUTH_HOST="https://${OPENSHIFT_DOMAIN}:8443"
        oc cluster up --server-loglevel=5 --public-hostname="${OPENSHIFT_DOMAIN}"
        oc login "${K8S_AUTH_HOST}" -u developer -p developer --insecure-skip-tls-verify=true
        export K8S_AUTH_API_KEY="$(oc whoami -t)"
        # Set OpenShift's environment variables for future steps
        echo "export OPENSHIFT_DOMAIN=${OPENSHIFT_DOMAIN}" >> $BASH_ENV
        echo "export K8S_AUTH_HOST=${K8S_AUTH_HOST}" >> $BASH_ENV
        echo "export K8S_AUTH_API_KEY=${K8S_AUTH_API_KEY}" >> $BASH_ENV
        source $BASH_ENV

version: 2
jobs:

{{ jobs }}

workflows:
  version: 2

  arnold:
    jobs:

{{ workflow_jobs }}
