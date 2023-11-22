FROM epitechcontent/epitest-docker:latest

WORKDIR /usr/app/src

COPY . .

RUN make

CMD ["sh", "-c", "./pbrain-gomoku-ai < ok.txt"]
