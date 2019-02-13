FROM golang:alpine AS builder
RUN export GOPATH=${HOME}/project1/chatbot
WORKDIR $GOPATH/chatbot/
RUN echo "etter workdir: " + $(pwd)
# Getting dependencies
RUN apk update && apk add --no-cache git
RUN go get -u github.com/bwmarrin/discordgo

ADD . .
# RUN GOOS=linux GOARCH=amd64 go build -ldflags="-w -s" -o /app/goapp
RUN pwd
RUN go build -o goapp
ENTRYPOINT ./goapp

# TODO: Make the image smaller
# final stage
# FROM scratch
# Copy our static executable.
# WORKDIR /app
# COPY --from=builder /app/goapp /app/
# Run the hello binary.
# RUN cd app/
# ENTRYPOINT ./goapp
