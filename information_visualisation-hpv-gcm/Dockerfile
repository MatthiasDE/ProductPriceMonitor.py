FROM alpine:3.14

WORKDIR /usr/src/app

RUN apk update
RUN apk add python3 py3-pip py3-pandas py3-matplotlib

COPY . .

CMD [ "python3", "./PPM-IV-HeisePV-GCM.py"]
