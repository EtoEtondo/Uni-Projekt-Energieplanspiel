FROM node:18.12-alpine

WORKDIR /app/frontend/frontend-energieplanspiel

COPY frontend-energieplanspiel/package.json .
COPY frontend-energieplanspiel/package-lock.json .

RUN npm install --silent

COPY frontend-energieplanspiel .

EXPOSE 5173

CMD npm run dev