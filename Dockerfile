FROM python:3.7-slim

USER root:root

RUN apt-get  -yqq --no-install-recommends install \
gcc=1.0.1 \
curl=1.1.1. \
wget 

# Installazione di pacchetti senza aggiornare prima l'indice (errore di best practice)
RUN sudo apt update && apt-get install -y git wget

# Non specifica un utente non privilegiato (tutto viene eseguito come root)
RUN mkdir /app

VOLUME /var/run/docker.sock://var/run/docker.sock

RUN cd /app/src

WORKDIR /app

ADD https://github.com/asottile/dockerfile /app/

# Copia di file sensibili non necessari nell'immagine
COPY ./secret_keys.txt /app/

USER root:root

# Esecuzione di una versione di Flask vulnerabile
RUN pip install flask==0.12

# Non vengono eseguite ottimizzazioni per ridurre le dimensioni dell'immagine

RUN nano

# Comando CMD poco chiaro e non ottimizzato
CMD python app.python




