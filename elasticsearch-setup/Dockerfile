FROM alpine/curl:latest

RUN apk add --no-cache bash
COPY update-passwords.sh update-passwords.sh

CMD ["bash", "update-passwords.sh"]