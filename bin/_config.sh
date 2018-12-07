#!/usr/bin/env bash

set -eo pipefail

# _set_minishift_path: add minishift path to the global PATH
function _set_minishift_path() {
    # We avoid using eval() in shell scripts, so we catch minishift's path to
    # binaries and we explictly add it to $PATH.
    MINISHIFT_PATH=$(minishift oc-env | grep -v \# | sed "s|export PATH=\"\(.*\):\$PATH\"|\1|")
    export PATH="$MINISHIFT_PATH:$PATH"
}

# _set_openshift_env: set OpenShift's environment
#
# Use this function to configure the OpenShift environment whenever your docker
# run commands require access to an OpenShift server. Nota bene: you'll need to
# login to your OpenShift server first.
function _set_openshift_env() {

    # Check that the current user is already logged in OpenShift
    if ! oc whoami &> /dev/null; then
        echo "Error: you need to login to an OpenShift server first."
        exit 1
    fi

    # Ansible's OpenShift raw module requires the following two environment
    # variables to be defined
    K8S_AUTH_API_KEY="$(oc whoami -t)"
    export K8S_AUTH_API_KEY
    K8S_AUTH_HOST=$(oc version | grep Server | awk '{print $2}')
    export K8S_AUTH_HOST

    # The OpenShift/k8s host is of the form https://domain:8443 so we can
    # extract the domain from it
    #
    # shellcheck disable=SC2034,SC2001
    OPENSHIFT_DOMAIN=$(echo "${K8S_AUTH_HOST}" | sed 's#https://\(.*\):8443#\1#')
    export OPENSHIFT_DOMAIN
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
# an OpenShift instance from Arnold's container (see Dockerfile).
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

    # Use docker tty option
    [[ "${USE_TTY}" == "false" ]] && TTY_OPTION="" || TTY_OPTION="-t"

    # Mount sources as a volume
    [[ "${MOUNT_SRC}" == "false" ]] && SRC_VOLUME_OPTION="" || SRC_VOLUME_OPTION="-v $PWD:/app"

    # If we wrap the SRC_VOLUME_OPTION with double quotes, this will break the
    # command, hence, we should ignore this rule here:
    #
    # shellcheck disable=SC2086
    docker run --rm -i ${TTY_OPTION} \
        -u "$(id -u)" \
        --env-file "$env_file" \
        --env K8S_AUTH_API_KEY \
        --env K8S_AUTH_HOST \
        --env OPENSHIFT_DOMAIN \
        ${SRC_VOLUME_OPTION} \
        -v "$HOME/.kube:/home/arnold/.kube" \
        "arnold:$(tr -d '\n' < VERSION)" \
        "${args[@]}"
}
