#!/usr/bin/env bash

set -eo pipefail

# _set_minishift_path: add minishift path to the global PATH
function _set_minishift_path() {
    # We avoid using eval() in shell scripts, so we catch minishift's path to
    # binaries and we explictly add it to $PATH.
    MINISHIFT_PATH=$(minishift oc-env | grep -v \# | sed "s|export PATH=\"\(.*\):\$PATH\"|\1|")
    export PATH="$MINISHIFT_PATH:$PATH"
}

# _docker_run: wrap docker run command
#
# usage: _docker_run [OPTIONS] [COMMAND]
#
#   OPTIONS: docker run options
#    --env-file: file to set environment variables (_e.g._ env.d/production)
#
#   COMMAND: command to be run in Arnold container (_e.g._ ansible-playbook deploy.yml)
#
# purpose:
#
# This utility improves the developer experience by dynamically setting
# environment variables required to run ansible playbooks and play with
# minishift from Arnold's container (see Dockerfile).
#
# prerequisite:
#
# To run this util, we suppose that:
#
#   - you are using minishift
#   - minishift has been already started (see bin/dev script)
#   - your have already logged in to your minishift instance via the oc login
#     command
function _docker_run() {

    local env_file="env.d/development"
    local args
    local i=1

    while [[ "$#" -ge "1" ]]; do
        local key="$1"
        shift

        case "$key" in
            --env-file=*)
                env_file="${key#*=}"
                ;;
            --env-file)
                env_file="$1"
                shift
                ;;
            *)
                args[i]=$key
                ;;
        esac
        i=$(( i+1 ))
    done

    # Check that the current user is already logged in OpenShift
    if ${OC_LOGIN} && ! oc whoami &> /dev/null; then
        echo "Error: you need to login to an OpenShift server first."
        exit 1
    fi

    [[ "$USE_TTY" == "false" ]] && TTY_OPTION="" || TTY_OPTION="-t"

    # Get the OpenShift host from OC
    OPENSHIFT_HOST=$(oc version | grep Server | awk '{print $2}')

    # The OpenShift host is of the form https://domain:8443 so we can
    # extract the domain from it
    # shellcheck disable=SC2034,SC2001
    OPENSHIFT_DOMAIN=$(echo "${OPENSHIFT_HOST}" | sed 's#https://\(.*\):8443#\1#')

    docker run --rm -i ${TTY_OPTION} \
        -u "$(id -u)" \
        --env-file "$env_file" \
        --env OC_LOGIN \
        --env K8S_AUTH_API_KEY="$(oc whoami -t)" \
        --env K8S_AUTH_HOST="${OPENSHIFT_HOST}" \
        --env OPENSHIFT_DOMAIN \
        -v "$PWD:/app" \
        "arnold:$(tr -d '\n' < VERSION)" \
        "${args[@]}"
}
