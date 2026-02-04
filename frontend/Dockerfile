FROM node:20-alpine

WORKDIR /app

# Install dependencies first for caching
COPY package.json package-lock.json ./
RUN npm ci

# Copy source
COPY . .

# Expose Vite port
EXPOSE 5173

# Start Dev Server with Host binding
CMD ["npm", "run", "dev", "--", "--host"]
