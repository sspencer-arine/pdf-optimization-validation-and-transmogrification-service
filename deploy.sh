#!/usr/bin/env bash

set -exu -o pipefail

sam build --config-file samconfig_dev.yaml
sam deploy --region us-east-1 --profile arine-dev --config-file samconfig_dev.yaml --stack-name sspencer-test
