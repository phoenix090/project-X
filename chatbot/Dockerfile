FROM golang:alpine AS builder
WORKDIR /app

# Getting dependencies
RUN apk update && apk add --no-cache git
RUN go get -u github.com/bwmarrin/discordgo

ADD . /app
# RUN GOOS=linux GOARCH=amd64 go build -ldflags="-w -s" -o /app/goapp
RUN cd /app && go build -o goapp
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
