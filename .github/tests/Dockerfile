FROM ubuntu:20.04
RUN apt update && \
  apt install iproute2 iputils-ping python3 -y

WORKDIR /usr/app

COPY . .

RUN ln -s /out /usr/app/out
RUN ln -s /in /usr/app/in

ENTRYPOINT [ "/usr/app/.github/tests/entrypoint.sh" ]
