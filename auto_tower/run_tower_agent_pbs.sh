#!/bin/bash

# Move to service tower directory
SCRIPT_PATH=$(realpath "$0")
SCRIPT_DIR=$(dirname "${SCRIPT_PATH}")
SERVICE_TOWER_DIR="${SCRIPT_DIR}/.tower"
mkdir -p "${SERVICE_TOWER_DIR}"
cd "${SERVICE_TOWER_DIR}"

set -euo pipefail

# Set the work directory
WORK_DIR="${SERVICE_TOWER_DIR}/work"

if [ ! -d "$WORK_DIR" ]; then
    echo "Creating work directory..."
    mkdir -p "$WORK_DIR"
    echo "Work directory created!"
fi

# Read the access token and session token from file
TOKEN_FILE="$HOME/.tower/token"
if [ ! -f "${TOKEN_FILE}" ]; then
    echo "Error: No connection ID file found at ${TOKEN_FILE}"
    exit 1
fi
CONNECTION_ID_FILE="${SERVICE_TOWER_DIR}/connection_id"
if [ ! -f "${CONNECTION_ID_FILE}" ]; then
    echo "Error: No connection ID file found at ${CONNECTION_ID_FILE}"
    exit 1
fi

TOWER_ACCESS_TOKEN=$(cat "$TOKEN_FILE")
CONNECTION_ID=$(cat "$CONNECTION_ID_FILE")

# Export the access token
export TOWER_ACCESS_TOKEN

# Download the agent if it doesn't exist
if [ ! -f tw-agent ]; then
  echo "Downloading tw-agent..."
  curl -fSL https://github.com/seqeralabs/tower-agent/releases/latest/download/tw-agent-linux-x86_64 > tw-agent
  chmod +x tw-agent
else
  echo "tw-agent already exists."
fi

# Run the agent with the specified work directory and connection ID
flock -n .lockfile ./tw-agent "$CONNECTION_ID" -u https://seqera.services.biocommons.org.au/api --work-dir="$WORK_DIR"
