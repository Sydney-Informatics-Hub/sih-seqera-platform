#!/bin/bash

# Move to script directory
SCRIPT_PATH=$(realpath "$0")
SCRIPT_DIR=$(dirname "${SCRIPT_PATH}")
SERVICE_TOWER_DIR="${SCRIPT_DIR}/.tower"
mkdir -p "${SERVICE_TOWER_DIR}"
cd "${SERVICE_TOWER_DIR}"

set -euo pipefail

WFHOST="setonix-workflow.pawsey.org.au"

# Get hostname
WFHOSTREAL=$(ssh ${WFHOST} hostname | grep -P "^setonix-\d+$" | tail -n 1)
ssh ${WFHOSTREAL} screen -dmS tower ${SCRIPT_DIR}/run_tower_agent.sh

echo "Tower agent is running within the screen session 'tower' on the workflow node '${WFHOSTREAL}'."
