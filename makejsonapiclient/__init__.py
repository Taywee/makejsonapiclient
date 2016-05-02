#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2016 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

import json
import sys

def make_json_api_client(
    api: list,
    outfile = sys.stdout,
    classname: str = "Client",
    imports: list = None,
    defaultclass: str = None,
    indent: str = '    ',
    ):

    if imports:
        outfile.writelines('{}\n'.format(imp.strip()) for imp in imports)
    outfile.write('\n')
    outfile.write('''class {name}(object):
{i}def __init__(self, scheme, host, port, username, password, httpclass{defaultclass}):
{i}{i}self.connection = httpclass(
{i}{i}{i}scheme=scheme,
{i}{i}{i}host=host,
{i}{i}{i}port=port,
{i}{i}{i}username=username,
{i}{i}{i}password=password,
{i}{i}{i})
'''.format(
            name=classname,
            defaultclass=(' = {}'.format(defaultclass) if defaultclass else ''),
            i=indent,
            )
        )
    outfile.write('\n')
