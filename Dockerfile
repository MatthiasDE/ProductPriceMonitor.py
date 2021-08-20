FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

#This is necessary to install numpy with pandas
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev
#---

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./PPM-DSC-HeisePV-GCM.py -r 3" ]