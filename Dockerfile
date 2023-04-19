FROM python:3.9.7-slim-buster
RUN git clone -b main https://github.com/naya1503/Ayra /home/Ayra/ \
    && chmod 777 /home/Ayra \
    && mkdir /home/Ayra/bin/

COPY ./.env.sample ./.env /home/Ayra/

WORKDIR /home/Ayra/

RUN pip3 install -U -r requirements.txt

CMD ["bash","start"]
