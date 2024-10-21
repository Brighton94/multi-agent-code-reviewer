#!/bin/bash

# Set project directory and image name
REPO_URL="https://github.com/your-repo/ai-code-reviewer.git"
PROJECT_DIR="$HOME/ai-code-reviewer"
IMAGE_NAME="ai-code-reviewer"

if [ ! -d "$PROJECT_DIR" ]; then
  echo "Cloning the repository..."
  git clone $REPO_URL $PROJECT_DIR
else
  echo "Repository already exists at $PROJECT_DIR"
fi

cd $PROJECT_DIR

echo "Building the Docker image..."
docker build -t $IMAGE_NAME .

echo "Setting up aliases..."

if ! grep -q "alias cr=" ~/.bashrc; then
  echo 'alias cr="docker run --rm -v \$(pwd):/app -w /app '"$IMAGE_NAME"' python /app/main.py"' >> ~/.bashrc
  echo "Added 'cr' alias to .bashrc"
else
  echo "'cr' alias already exists in .bashrc"
fi

if ! grep -q "alias mrs=" ~/.bashrc; then
  echo 'alias mrs="docker run --rm -v \$(pwd):/app -w /app '"$IMAGE_NAME"' python /app/src/mr-summarizer.py"' >> ~/.bashrc
  echo "Added 'mrs' alias to .bashrc"
else
  echo "'mrs' alias already exists in .bashrc"
fi

echo "Sourcing .bashrc to apply changes..."
source ~/.bashrc

echo "Installation and setup complete! You can now use the 'cr' and 'mrs' commands."

echo "Verifying Docker image..."
docker images | grep $IMAGE_NAME