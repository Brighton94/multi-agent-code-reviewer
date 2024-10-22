#!/bin/bash

PROJECT_DIR=$(pwd)

if ! command -v poetry &> /dev/null; then
  echo "Poetry is not installed. Installing Poetry..."
  pip install poetry
else
  echo "Poetry is already installed"
fi

echo "Installing project dependencies with Poetry..."
poetry install

if ! grep -q "alias cr=" ~/.bashrc; then
  echo 'alias cr="python3 $PROJECT_DIR/main.py"' >> ~/.bashrc
  echo "Added 'cr' alias to .bashrc"
else
  echo "'cr' alias already exists in .bashrc"
fi

if ! grep -q "alias mrs=" ~/.bashrc; then
  echo 'alias mrs="python3 $PROJECT_DIR/src/mr-summarizer.py"' >> ~/.bashrc
  echo "Added 'mrs' alias to .bashrc"
else
  echo "'mrs' alias already exists in .bashrc"
fi

echo "Sourcing .bashrc to apply changes..."
source ~/.bashrc

echo "Setup complete! You can now use the 'cr' and 'mrs' commands."