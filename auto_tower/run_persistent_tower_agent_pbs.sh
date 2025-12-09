#!/bin/bash

# Move to script directory
SCRIPT_PATH=$(realpath "$0")
SCRIPT_DIR=$(dirname "${SCRIPT_PATH}")
SERVICE_TOWER_DIR="${SCRIPT_DIR}/.tower"
mkdir -p "${SERVICE_TOWER_DIR}"
cd "${SERVICE_TOWER_DIR}"

set -euo pipefail

# Try creating a persistent session
# If it exists, continue
{
    persistent-sessions start nf-tower > ps_start.out 2> ps_start.err
} || {
    EXISTS="$(grep 'session exists' ps_start.err)"
    if [ ! "${EXISTS}" == "0" ]; then
        echo "Persistent session already exists."
    else
        echo "An error occured and the persistent session could not be created. Exiting."
        exit 1
    fi
}

PSHOST="nf-tower.${USER}.${PROJECT}.ps.gadi.nci.org.au"
ssh ${PSHOST} screen -dmS tower ${SCRIPT_DIR}/run_tower_agent_pbs.sh

echo "Tower agent is running within the screen session 'tower' on the persistent session '${PSHOST}'."
