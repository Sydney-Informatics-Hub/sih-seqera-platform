#!/bin/bash

cd $(realpath "$0")

quarto render . --execute-params params.yaml