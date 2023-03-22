#!/bin/bash

eval "$(conda shell.bash hook)"
conda activate stl

streamlit run main.py --server.port 8080
