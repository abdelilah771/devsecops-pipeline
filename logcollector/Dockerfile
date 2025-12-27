# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /usr/src/app

COPY package*.json ./

# Install all dependencies including devDependencies (if any needed for build)
# Using ci for reproducible builds
RUN npm ci
RUN npx prisma generate

COPY . .

# Stage 2: Production
FROM node:18-alpine

WORKDIR /usr/src/app

COPY package*.json ./

# Install only production dependencies
RUN npm ci --only=production

# Copy source code from builder stage
COPY --from=builder /usr/src/app .

EXPOSE 3000

# Use tini as entrypoint for better signal handling
RUN apk add --no-cache tini
ENTRYPOINT ["/sbin/tini", "--"]

CMD ["node", "server.js"]
