FROM node:20-slim

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Expose Vite default port
EXPOSE 5173

# Run Vite dev server with host exposed
CMD ["npm", "run", "dev", "--", "--host"]
