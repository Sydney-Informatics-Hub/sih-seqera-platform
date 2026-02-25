#!/bin/bash

cd $(dirname $(realpath "$0"))

quarto render . --execute-params params.yaml