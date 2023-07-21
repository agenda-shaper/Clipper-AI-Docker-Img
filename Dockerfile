FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime


WORKDIR /

# add media
ADD bottom_clips /bottom_clips
ADD audio /audio

# install ffmepg
RUN apt-get update && apt-get install -y git ffmpeg

RUN pip3 install --upgrade pip
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# runpod main file
ADD handler.py .

# my code
ADD app.py .

CMD [ "python", "-u", "/handler.py" ]