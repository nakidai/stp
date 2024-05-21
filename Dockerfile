FROM python:3.12-alpine
WORKDIR /app

RUN apk add --no-cache cairo
COPY . .
RUN pip install --break-system-packages --no-cache-dir .

CMD ["wastp", "-p", "80"]
EXPOSE 80
