# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on: Python3 and Requests
RUN \
  apk add --no-cache \
    python3 py3-requests

# Copy files required for add-on
COPY run.sh /
COPY sl2ha.py /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]