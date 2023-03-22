#!/bin/bash
export STREAMLIT_SERVER_PORT=80
export STREAMLIT_SERVER_PORT=8080
export PATH="/home/ubuntu/miniconda3/bin:$PATH"
eval "$(conda shell.bash hook)"
conda activate stl

streamlit run main.py --server.port 8080
