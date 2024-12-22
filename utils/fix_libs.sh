#!/bin/bash

PYTHON_PATH=$(which python)

BGE_M3_PATH="${PYTHON_PATH%/bin/python}/lib/python3.12/site-packages/milvus_model/hybrid/bge_m3.py"

FIXED_BGE_M3_PATH="./utils/bge_m3.py"

cp -f "$FIXED_BGE_M3_PATH" "$BGE_M3_PATH"