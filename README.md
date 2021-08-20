# ProductPriceMonitor.py
Aggregated Product Price Monitor for Graphic Cards


## Build
```bash
docker build -t ppm-dsc-hpv-gcm.py .
```

## Run
According to baseline:
```bash
docker run --entrypoint <entrypoint.sh> <image:tag> <arg1> <arg2> <arg3>
-v [host directory]:[container directory]
```
Option 1: Interactive with TTY
```bash
docker run -v ~:/usr/src/app/db -it --entrypoint python ppm-dsc-hpv-gcm.py ./PPM-DSC-HeisePV-GCM.py -f ./db/product_price_monitor.db -r 3

Option 2: In Background
```bash
docker run -d -v ~:/usr/src/app/db ppm-dsc-hpv-gcm.py
docker exec -it <container name> sh

Combine all :D:
```bash
docker run -d -v ~:/usr/src/app/db --entrypoint python ppm-dsc-hpv-gcm.py ./PPM-DSC-HeisePV-GCM.py -f ./db/product_price_monitor.db -r 3
```

# Monitoring
```bash
docker logs <container name>
docker inspect <container name>
```

You might be interested that you use "-f" with the logs command to follow the logs continuously.

## Cleaning up
```bash
docker container stop ppm-dsc-hpv-gcm.py
docker container rm ppm-dsc-hpv-gcm.py
docker volume rm <volumename>
```
