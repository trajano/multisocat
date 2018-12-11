# multisocat

A socat image that runs on multiple ports.

## Design

As `nobody` but can be overriden by `user` option.

For each environment variable that starts with `SOCAT_` spawn off an instance of `SOCAT_` with those parameters. Note that order is not guaranteed.

Have `nc` installed to allow creation of `HEALTHCHECK`.  (A good addition to this image is a small shell script that will just do `nc -z` given a list of ports locally and verify that they are all open, maybe in a future release or PR)

Additionally provide `BLACKHOLE_TCP` and `BLACKHOLE_UDP` which provides a comma separated list of ports to listen but not respond to.  Primarily used for testing.  These would be implemented as `nc -l` and `nc -ul` respectively.

Wait for all those socat instances to finish.

## Example

Here is an example of a service that forwards to a remote logstash/graylog server that exposes several ports.

    version: '3.7'
    services:
      log:
        image: trajano/multisocat
        user: root
        environment:
          SOCAT_BEATS: "TCP-LISTEN:5044,fork TCP:202.54.1.5:5044"
          SOCAT_TEXT: "TCP-LISTEN:5555,fork TCP:202.54.1.5:5555"
          SOCAT_GELF: "UDP-LISTEN:12201,fork UDP:202.54.1.5:12201"
          BLACKHOLE_TCP: "514,50000"
          BLACKHOLE_UDP: "514,60000"
        healthcheck:
          test: nc -z localhost 5044

Note that the user needs to be `root` in order for ports less than 1024 to be openned.
