#!/usr/bin/env bash

set -eo pipefail

# _set_env: set minishift environment
function _set_minishift_env() {
    # We avoid using eval() in shell scripts, so we catch minishift's path to
    # binaries and we explictly add it to $PATH.
    MINISHIFT_PATH=$(minishift oc-env | grep -v \# | sed "s|export PATH=\"\(.*\):\$PATH\"|\1|")
    export PATH="$MINISHIFT_PATH:$PATH"
}

# _configure_environment: configure environment file to use with Docker
#
# usage: _configure_environment [environment]
#
# environment: target environment file name (e.g. development for
# env.d/development)
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
}

# _docker_run: wrap docker run command
#
# usage: _docker_run [options] [ARGS...]
#
# options: docker run command options
# ARGS   : docker run command arguments
#
# DISCLAIMER:
#
# /!\ DO NOT USE THIS UTILITY FOR A PRODUCTION ENVIRONMENT /!\
#
# This utility function is only meant to get used by developers on their local
# machine to test various OpenShift configurations or instances.
#
# PURPOSE:
#
# This utility improves the developer experience by dynamically generating
# environment variables required to run ansible playbooks and play with
# minishift from Arnold's container (see Dockerfile).
#
# PREREQUISITE:
#
# To run this util, we suppose that:
#
#   - you are using minishift
#   - minishift has been already started (see bin/dev script)
#   - your have already logged in to your minishift instance via the oc login
#     command
function _docker_run() {

    _set_minishift_env
    _configure_environment

    # Check that minishift is running
    if ! minishift status | grep Running > /dev/null ; then
        echo "Error: minishift is not running. Please start it first."
        exit 1
    fi

    # Check that the current user is already logged in minishift
    if ! oc whoami &> /dev/null; then
        echo "Error: you need to login to minishift first."
        exit 1
    fi

    docker run --rm -it \
        -u $(id -u) \
        --env-file $env_file \
        --env K8S_AUTH_API_KEY=$(oc whoami -t) \
        --env K8S_AUTH_HOST="https://$(minishift ip):8443" \
        --env MINISHIFT_IP="$(minishift ip)" \
        -v $PWD:/app \
        arnold:$(tr -d '\n' < VERSION) \
        "$@"
}
