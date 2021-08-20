# ProductPriceMonitor.py
Aggregated Product Price Monitor for Graphic Cards


##Build
docker build -t ppm-dsc-hpv-gcm.py .


##Run
According to baseline:
  docker run --entrypoint <entrypoint.sh> <image:tag> <arg1> <arg2> <arg3>
  -v [host directory]:[container directory]

Option 1: Interactive with TTY
docker run -v ~:/usr/src/app/db -it --entrypoint python ppm-dsc-hpv-gcm.py ./PPM-DSC-HeisePV-GCM.py -f ./db/product_price_monitor.db -r 3

Option 2: In Background
docker run -d -v ~:/usr/src/app/db ppm-dsc-hpv-gcm.py
docker exec -it <container name> sh

Combine all :D:
docker run -d -v ~:/usr/src/app/db --entrypoint python ppm-dsc-hpv-gcm.py ./PPM-DSC-HeisePV-GCM.py -f ./db/product_price_monitor.db -r 3


##Cleaning up
 docker container stop ppm-dsc-hpv-gcm.py
 docker container rm ppm-dsc-hpv-gcm.py
 docker volume rm <volumename>
