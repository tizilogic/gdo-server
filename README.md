# gdo-server

THIS IS A WORK IN PROGRESS...

Simple Server to securely control GPIO on RPi Hardware.
I use this to open my garage door at home. Used together
with [gdo-client](https://github.com/tizilogic/gdo-client)
but also provides a rudimentary web interface to use as 
standalone.

## The Setup

I use an old Raspberry Pi model B that I have hooked up to
my remote control for the garage door. I run Apache2 on it
together with mod_wsgi to run my server software, that enables
clients to connect and activate the GPIO pin that is being 
used to activate the remote for the garage.

## Trying to stay "safe"

Since I really don't want anyone else opening my garage door,
I tried to implement a couple of safe guards to prevent common
attacks:

1. I'm using [letsencrypt](https://letsencrypt.org/) to encrypt
web traffic.
1. A pin can only be activated with a passphrase *(don't worry
it isn't the one found on this repo... I use a crazy long one
irl.)*
1. The server provides 64 bytes of `salt` that is valid for 60 
seconds and can only be used once. *(The `salt` comes from 
`/dev/urandom` and the server waits for a random fraction of
a second before sending the `salt`, to make it more robust
against timing attacks)*
1. `SHA3-512` is being used together with the `salt` for 
transmitting the salted and hashed passphrase.

Those are the safeguards I was able to come up with, but as it
stands with cryptography, usually something believed to be safe
in reality ever so often isn't, so fingers crossed. 
