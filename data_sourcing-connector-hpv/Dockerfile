FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

#This is necessary to install numpy with pandas
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev
#---

#This is necessary to install lxml
RUN apk add libxml2-dev libxslt-dev python3-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "PPM-DSC-HeisePV-GCM.py", "-f", "./db/product_price_monitor.db", "-r", "3" ]