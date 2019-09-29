#!/usr/bin/env bash
#
# Helper functions to ease-up container usage

set -o errexit


get_backend_id () {
  local container_id=$(docker ps | grep personal_site | awk '{print $1}')
  if [[ ! "$container_id" ]]; then
    1>&2 echo "There is no running back-end container, quitting."
    exit 1
  else
    echo "$container_id"
  fi
}

run_management_command () {
  local passed_arguments="${@:-}"
  if [[ ! "$passed_arguments" ]]; then
    1>&2 echo "No command supplied, quitting"
    exit 1
  fi
  container_id=$(get_backend_id)
  exec docker exec -it "$container_id" python3 manage.py $passed_arguments
}


run_management_command "$@"
