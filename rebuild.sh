#!/usr/bin/bash
mkdir dist
yes | pip uninstall pact
yes | python -m build
yes | pip install dist/pact-0.0.1-py3-none-any.whl
rm -r dist
