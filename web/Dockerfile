FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci
RUN npm install -g @angular/cli

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist/web/browser /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80