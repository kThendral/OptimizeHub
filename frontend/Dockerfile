# Use official Node.js image as base
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files only (for better caching)
COPY package*.json ./

# Clean install all dependencies inside container (no local node_modules)
RUN npm install

# Copy all source files (local node_modules excluded by .dockerignore)
COPY . .

# Expose Vite port
EXPOSE 5173

# Start Vite dev server with host binding for Docker
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
