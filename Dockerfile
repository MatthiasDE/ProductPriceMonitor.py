FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

#This is necessary to install numpy with pandas
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev
#---

COPY . .

CMD [ "python", "./PPM-IV-HeisePV-GCM.py" ]