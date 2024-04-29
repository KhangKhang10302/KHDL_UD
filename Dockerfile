FROM python:3.9
WORKDIR /app
COPY r.txt ./
RUN pip install -r r.txt 
COPY cao.py ./
CMD ["python", "cao.py"]
# docker build . -f Dockerfile -t cao_test:version_1
# docker build --no-cache . -f Dockerfile -t cao_test:version_1

# docker images|grep cao  
# docker image rm c8
# docker tag cao_test:version_1 khangkhang10302/cao_test:version_1
# docker login

# docker push khangkhang10302/cao_test:version_1
# docker ps|grep cao
# docker ps -a|grep cao
# docker compose logs