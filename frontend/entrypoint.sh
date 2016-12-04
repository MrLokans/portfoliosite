#!/bin/bash
set -e
cd /static/
gulp
exec "$@"