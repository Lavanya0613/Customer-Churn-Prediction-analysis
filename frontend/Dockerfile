# Build stage
FROM node:20-alpine as build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copy source and build
COPY . .
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# Production stage - use nginx to serve static files
FROM nginx:alpine

# Copy built files from the build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom nginx configuration if you have routing (optional but recommended for SPA)
# We will use default nginx config which works for basic Vite builds without complex routing
# But for a real React app with React Router, you'd need a custom nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
