#!/usr/bin/env bash

set -eo pipefail

# _set_minishift_path: add minishift path to the global PATH
function _set_minishift_path() {
    # We avoid using eval() in shell scripts, so we catch minishift's path to
    # binaries and we explictly add it to $PATH.
    MINISHIFT_PATH=$(minishift oc-env | grep -v \# | sed "s|export PATH=\"\\(.*\\):\$PATH\"|\\1|")
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
#   OPTIONS:
#     -e [ENV_FILE] file to set environment variables (_e.g._ env.d/production)
#     -m            mount sources as a volume
#     -t            allocate a pseudo-TTY while running command
#     -v            verbose mode
#   COMMAND:
#     Any command to be run in Arnold container (_e.g._ ansible-playbook deploy.yml)
#
# example:
#
# The following example will run the `ls` command in Arnold's container with
# local sources mounted as a volume in the container (-m option) and allocating
# a TTY, thus allowing to use bash pipes with docker commands. The verbose mode
# (-v option) will display the command to execute prior to execute it.
#
#   $ _docker_run -mtv -e env.d/production ls
#
# purpose:
#
# This utility improves the developer experience by dynamically setting
# environment variables required to run ansible playbooks and play with an
# OpenShift instance from Arnold's container (see Dockerfile).
function _docker_run() {

    local env_file="env.d/development"
    local src_volume_option=""
    local tty_option=""
    local verbose=0

    # Parse options
    while getopts "e:mtv" opt; do
        case ${opt} in
            e)
                env_file="${OPTARG}";;
            m)
                src_volume_option="-v ${PWD}:/app";;
            t)
                tty_option="-t";;
            v)
                verbose=1;;
            \?)
                echo "Invalid option '-${OPTARG}'" 1>&2
                exit 1;;
        esac
    done
    shift $((OPTIND -1))

    # The command to run in a docker container
    local cmd
    cmd=( "$@" )

    # The whole docker-run-wrapped command
    local run
    run="docker run --rm -i ${tty_option} \
        -u $(id -u) \
        --env-file ${env_file} \
        --env K8S_AUTH_API_KEY \
        --env K8S_AUTH_HOST \
        --env OPENSHIFT_DOMAIN \
        ${src_volume_option} \
        -v ${HOME}/.kube:/home/arnold/.kube \
        arnold:$(tr -d '\n' < VERSION) \
        ${cmd[*]}"

    if [[ verbose -eq 1 ]]; then
        echo -e "\\033[0;33m🚀 command:\\n ${run}\\033[0m" | sed -e 's/[[:space:]]\+/ /g'
    fi
    eval "${run}"
}

# _ansible_playbook: wrap docker run ansible-playbook command
#
# usage: _ansible_playbook [OPTIONS] [ARGS]
#
#   OPTIONS: Any valid ansible-playbook option
#
#   ARGS: Any valid ansible-playbook argument
#
# This commands is executed in a docker container that mounts the local
# directory as a volume and creates a pseudo-TTY.
function _ansible_playbook(){
    _docker_run -mt ansible-playbook "$@"
}

# _ci_ansible_playbook: wrap docker run ansible-playbook command for the CI
#
# usage: _ansible_playbook [OPTIONS] [ARGS]
#
#   OPTIONS: Any valid ansible-playbook option
#
#   ARGS: Any valid ansible-playbook argument
#
# This commands is executed in a docker container that loads env.d/ci file
# environment variable definitions. Ansible env_type is forced to "ci". The
# vault password is always prompted.
function _ci_ansible_playbook(){
    _docker_run -e "env.d/ci" ansible-playbook --ask-vault-pass -e "env_type=ci" "$@"
}
