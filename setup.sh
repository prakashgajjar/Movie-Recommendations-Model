#!/bin/bash

# Create .streamlit directory
mkdir -p ~/.streamlit/

# Create Streamlit config
echo "\
[server]\n\
port = \$PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml
