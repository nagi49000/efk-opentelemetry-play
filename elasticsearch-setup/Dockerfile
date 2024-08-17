FROM alpine/curl:latest

RUN apk add --no-cache bash
COPY --chown=elasticsearch:root update-passwords.sh update-passwords.sh

CMD ["bash", "update-passwords.sh"]