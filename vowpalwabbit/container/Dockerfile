# Build an image that can do training and inference in SageMaker
# This is a Python 3 image that uses the nginx, gunicorn, flask stack
# for serving inferences in a stable way.

FROM ubuntu:18.10


RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         python3 \ 
         nginx \
         ca-certificates \
         vowpal-wabbit \
         python3-venv \
         python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#RUN apt-get install -y --no-install-recommends python3-venv python3-pip && apt-get clean
# python  3.6.6
# didn't work couldn't find sysconfig...

#RUN pip3 install -r scripts/requirements-pipeline.txt

#get warning
#Problem unlinking the file /var/cache/apt/archives/partial/.apt-acquire-privs-test.iGgLKo

# Here we get all python packages.
# There's substantial overlap between scipy and numpy that we eliminate by
# linking them together. Likewise, pip leaves the install caches populated which uses
# a significant amount of space. These optimizations save a fair amount of space in the
# image, which reduces start up time.
#RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py && \
RUN    pip3 install numpy==1.15.4 scipy scikit-learn pandas flask gevent gunicorn && \
        (cd /usr/local/lib/python3.6/dist-packages/scipy/.libs; rm *; ln ../../numpy/.libs/* .) && \
        rm -rf /root/.cache

# Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# ENTRYPOINT PYTHONPATH=zalondatatools:$PYTHONPATH python3 scripts/ranking_pipeline.py
# CMD /bin/bash

# Set up the program in the image
COPY vowpalwabbit /opt/program
WORKDIR /opt/program

COPY . /opt/program
WORKDIR /opt/program
