FROM node:18.12-alpine as build

WORKDIR /app/frontend/frontend-energieplanspiel

COPY frontend-energieplanspiel/package.json .
COPY frontend-energieplanspiel/package-lock.json .

RUN npm install --silent

COPY frontend-energieplanspiel .

RUN npm run build


FROM nginx:stable-alpine

COPY --from=build /app/frontend/frontend-energieplanspiel/dist /var/www/energieplanspiel

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx/my-site.crt /etc/ssl/certs/my-site.crt
COPY nginx/my-site.key /etc/ssl/private/my-site.key

CMD ["nginx", "-g", "daemon off;"]