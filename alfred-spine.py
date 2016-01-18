#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import zmq


def main(cli_args):
    try:
        spine_input, spine_output = init_io(cli_args)

        print "Ready"

        while True:
            message = spine_input.recv_string()
            print "SPINE:" + message
            if message:
                spine_output.send_string(message)

    except KeyboardInterrupt:
        pass


def init_io(cli_args):
    old_umask = os.umask(007)

    input_socket_addr = get_arg_by_index_or_default_env(cli_args, 1, 'ALFRED_SPINE_INPUT')
    spine_input = init_socket(input_socket_addr, zmq.PULL)

    output_socket_addr = get_arg_by_index_or_default_env(cli_args, 2, 'ALFRED_SPINE_OUTPUT')
    spine_output = init_socket(output_socket_addr, zmq.PUB)

    os.umask(old_umask)

    return spine_input, spine_output


def get_arg_by_index_or_default_env(cli_args, arg_index, env_key):
    if len(cli_args) > arg_index:
        return cli_args[arg_index]
    else:
        try:
            os.environ[env_key]
        except KeyError:
            sys.exit("Could not find Alfred's input socket from cli nor env var " + env_key)


def init_socket(addr, zmq_mode):
    socket = zmq.Context().socket(zmq_mode)
    socket.bind(addr)

    print "ZMQ socket\t" + str(zmq_mode) + " bound to " + addr

    return socket


if __name__ == '__main__':
    main(sys.argv)
