FROM node:20-alpine

WORKDIR /app

# 의존성 설치
COPY package*.json ./
RUN npm install

# 코드 복사
COPY . .

EXPOSE 3000

CMD ["npx", "next", "dev", "--hostname", "0.0.0.0"]
