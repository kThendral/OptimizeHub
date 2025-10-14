# Build the Docker image
# (run this in the project root)
docker build -t optimizehub .

# Run the container
# (exposes Vite dev server on localhost:5173)
docker run -p 5173:5173 optimizehub

# Or use Docker Compose
# (recommended for development)
docker-compose up --build

# Stop and remove containers
# (when finished)
docker-compose down
