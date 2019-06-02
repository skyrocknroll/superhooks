#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################

# A event listener meant to be subscribed to PROCESS_STATE_CHANGE
# events.  It will send web hook messages when processes that are children of
# supervisord transition unexpectedly to the EXITED state.

# A supervisor config snippet that tells supervisor to use this script
# as a listener is below.
#
# [eventlistener:superhooks]
# command=python superhooks -u http://localhost:8090/ -e BACKOFF,STOPPING,FATAL,EXITED,STOPPED,UNKNOWN -i 1 -d a:b::c:d -H p:q::r:s
# events=PROCESS_STATE,TICK_60

"""
Usage: superhooks [-u url] [-e events]

Options:
  -h, --help            show this help message and exit
  -u URL, --url=URL
                   Web hook URL

  -e EVENTS, --events=EVENTS
                        Supervisor process state event(s)
"""

import copy
import os
import sys

import requests
from superlance.process_state_monitor import ProcessStateMonitor
from supervisor import childutils


class SuperHooks(ProcessStateMonitor):
    SUPERVISOR_EVENTS = (
        'STARTING', 'RUNNING', 'BACKOFF', 'STOPPING',
        'FATAL', 'EXITED', 'STOPPED', 'UNKNOWN',
    )

    @classmethod
    def _get_opt_parser(cls):
        from optparse import OptionParser

        parser = OptionParser()
        parser.add_option("-u", "--url", help="Web Hook URL")
        parser.add_option("-d", "--data", help="data in key value pair ex: `foo:bar::goo:baz`")
        parser.add_option("-H", "--headers", help="headers in key value pair ex: `foo:bar::goo:baz`")
        parser.add_option("-e", "--events",
                          help="Supervisor event(s). Can be any, some or all of {} as comma separated values".format(
                              cls.SUPERVISOR_EVENTS))

        return parser

    @classmethod
    def parse_cmd_line_options(cls):
        parser = cls._get_opt_parser()
        (options, args) = parser.parse_args()
        return options

    @classmethod
    def validate_cmd_line_options(cls, options):
        parser = cls._get_opt_parser()
        if not options.url:
            parser.print_help()
            sys.exit(1)
        if not options.events:
            parser.print_help()
            sys.exit(1)

        validated = copy.copy(options)
        return validated

    @classmethod
    def get_cmd_line_options(cls):
        return cls.validate_cmd_line_options(cls.parse_cmd_line_options())

    @classmethod
    def create_from_cmd_line(cls):
        options = cls.get_cmd_line_options()

        if 'SUPERVISOR_SERVER_URL' not in os.environ:
            sys.stderr.write('Must run as a supervisor event listener\n')
            sys.exit(1)

        return cls(**options.__dict__)

    def __init__(self, **kwargs):
        ProcessStateMonitor.__init__(self, **kwargs)
        self.url = kwargs['url']
        self.data = kwargs.get('data', None)
        self.headers = kwargs.get('headers', None)
        events = kwargs.get('events', None)
        self.process_state_events = [
            'PROCESS_STATE_{}'.format(e.strip().upper())
            for e in events.split(",")
            if e in self.SUPERVISOR_EVENTS
        ]

    def get_process_state_change_msg(self, headers, payload):
        pheaders, pdata = childutils.eventdata(payload + '\n')
        pheaders_all = ""
        for k, v in pheaders.items():
            pheaders_all = pheaders_all + k + ":" + v + " "
        return "{groupname}:{processname};{from_state};{event};{pheaders_all}".format(
            event=headers['eventname'], pheaders_all=pheaders_all, **pheaders
        )

    def send_batch_notification(self):
        for msg in self.batchmsgs:
            processname, from_state, eventname, pheaders_all = msg.rsplit(';')
            params = {'process_name': processname, 'from_state': from_state, 'event_name': eventname,
                      'pheaders_all': pheaders_all}
            if self.data:
                for item in self.data.split("^^"):
                    kv = item.split("^")
                    if len(kv) == 2:
                        params[kv[0]] = kv[1]
            headers = {}
            if self.headers:
                for item in self.headers.split("^^"):
                    kv = item.split("^")
                    if len(kv) == 2:
                        headers[kv[0]] = kv[1]
            requests.post(self.url, data=params, headers=headers)


def main():
    superhooks = SuperHooks.create_from_cmd_line()
    superhooks.run()


if __name__ == '__main__':
    main()
