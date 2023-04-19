FROM theteamultroid/ultroid:main

RUN git clone https://github.com/naya1503/Ayra /home/Ayra/ \
    && chmod 777 /home/Ayra \
    && mkdir /home/Ayra/bin/

WORKDIR /home/Ayra/

RUN pip3 install -U -r requirements.txt

CMD ["bash","start"]