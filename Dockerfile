FROM python:3.7-alpine
RUN apk add --no-cache bash netcat-openbsd socat
CMD [ "/multisocat" ]
COPY multisocat.py /multisocat
RUN chmod 0755 /multisocat
USER nobody
