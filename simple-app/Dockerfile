FROM ubuntu:22.04

RUN apt-get update && apt-get install -y iputils-ping
RUN useradd -ms /bin/bash dirac
USER dirac
CMD ["tail", "-f", "/dev/null"]