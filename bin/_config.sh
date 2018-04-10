#!/usr/bin/env bash

set -eo pipefail

# _configure_environment: configure environment file to use with Docker
#
# usage: _configure_environment [environment]
#
# environment: target environment file name (e.g. development for env.d/development)
function _configure_environment() {

    environment=${1:-development}
    env_file="env.d/${environment}"

    if [[ ! -e $env_file ]]; then
        echo "Environment file ${env_file} does not exists. You should create it first:"
        echo ""
        echo "  $ cp env.d/base env.d/${environment}"
        echo ""
        echo "And then edit it with relevant values."
        exit 1
    fi

    sed -i -E "s/(K8S_AUTH_API_KEY=)(.*)/\1$(oc whoami -t)/" $env_file
    sed -i -E "s/(K8S_AUTH_HOST=)(.*)/\1https:\/\/$(minishift ip):8443/" $env_file
}

# _docker_run: wrap docker run command
#
# usage: _docker_run [options] [ARGS...]
#
# options: docker run command options
# ARGS   : docker run command arguments
function _docker_run() {
    _configure_environment
    docker run --rm -it --env-file $env_file arnold:$(tr -d '\n' < VERSION) "$@"
}
