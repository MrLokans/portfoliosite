#!/bin/bash
set -e
cd /frontend/
gulp
exec "$@"