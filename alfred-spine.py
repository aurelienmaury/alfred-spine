#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
import sys
import os

input_socket = sys.argv[1]
input_source = "cli"

if not input_socket:
    input_socket = os.environ['ALFRED_SPINE_INPUT']
    output_source = "env"
    if not input_socket:
        sys.exit("Could not find Alfred's input socket from cli nor env var (ALFRED_SPINE_INPUT)")

spine_input = zmq.Context().socket(zmq.PULL)
spine_input.bind(input_socket)
print "Bound to:\t" + input_socket

output_socket = sys.argv[2]
output_source = "cli"

if not output_socket:
    output_socket = os.environ['ALFRED_SPINE_OUPUT']
    output_source = "env"
    if not output_socket:
        sys.exit("Could not find Alfred's output socket from cli nor env var (ALFRED_SPINE_OUTPUT)")

print "Publishing on:\t" + output_socket

spine_output = zmq.Context().socket(zmq.PUB)
spine_output.bind(output_socket)


def main():
    try:
        print "Ready"
        while True:
            message = spine_input.recv_string()
            print "SPINE:" + message
            if message:
                spine_output.send_string(message)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
