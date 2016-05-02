#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2016 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

import json
import re
import sys

_formatpattern = re.compile(r'\{([a-zA-Z]\w*)\}')

def make_json_api_client(
    api: list,
    outfile = sys.stdout,
    classname: str = "Client",
    imports: list = None,
    defaultclass: str = None,
    indent: str = '    ',
    withcontext: bool = False,
    ):

    if imports:
        outfile.writelines('{}\n'.format(imp.strip()) for imp in imports)

    outfile.write('\n')
    outfile.write('''from . import urlquote

class {name}(object):
{i}_NO_VALUE = object()
{i}
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

    if withcontext:
        outfile.write('''
{i}def __enter__(self):
{i}{i}self._old_connection = self.connection
{i}{i}self.connection = self.connection.__enter__()
{i}{i}return self

{i}def __exit__(self, type, value, traceback):
{i}{i}self._old_connection.__exit__(type, value, traceback)
{i}{i}self.connection = self._old_connection
{i}{i}del self._old_connection
'''.format(
            name=classname,
            defaultclass=(' = {}'.format(defaultclass) if defaultclass else ''),
            i=indent,
            )
        )

    outfile.write('\n')

    # Build the API endpoint
    for endpoint in api:
        # Get basename of method
        if endpoint.get('name'):
            basename = endpoint['name']
        else:
            basename = endpoint['endpoint']

        queryargs = _formatpattern.findall(endpoint['endpoint'])

        # Get or infer methods
        if endpoint.get('methods'):
            methods = frozenset(endpoint['methods'])
        else:
            if endpoint.get('json-args') or endpoint.get('json-options'):
                methods = frozenset({'GET', 'PUT', 'DELETE'})
            else:
                methods = frozenset(('GET',))

        json_args = endpoint.get('json-args', [])
        json_options = endpoint.get('json-options', [])

        defaults = endpoint['defaults'] if 'defaults' in endpoint else dict()

        for method in methods:
            jsonmethod = method in {'PUT', 'POST'}
            usedvars = set()

            defname = '{meth}_{name}'.format(meth=method.lower(), name=basename.lower().replace('-', '_'))
            args = ['self']

            for arg in queryargs:
                if arg not in usedvars:
                    argitem = arg
                    if arg in defaults:
                        argitem += ' = {}'.format(repr(defaults[arg]))

                    args.append(argitem)
                    usedvars.add(arg)

            if jsonmethod:
                for arg in json_args:
                    if arg not in usedvars:
                        argitem = arg
                        if arg in defaults:
                            argitem += ' = {}'.format(repr(defaults[arg]))

                        args.append(argitem)
                        usedvars.add(arg)


                for option in json_options:
                    if option not in usedvars:
                        optitem = option
                        if optitem in defaults:
                            optitem += ' = {}'.format(repr(defaults[option]))
                        else:
                            optitem += ' = self._NO_VALUE'

                        args.append(optitem)
                        usedvars.add(option)

            outfile.write('\n{i}def {name}({args}):\n'.format(i=indent, name=defname, args=', '.join(args)))
            outfile.write('{i}{i}_api_endpoint = "{endpoint}".format({queryargs})\n'.format(
                i=indent,
                endpoint=endpoint['endpoint'],
                queryargs=', '.join('{arg}=urlquote({arg})'.format(arg=arg) for arg in queryargs)))

            if jsonmethod:
                outfile.write('{i}{i}_all_json_args = {{{args}}}\n'.format(
                    i=indent,
                    args=', '.join("'{arg}': {arg}".format(arg=arg) for arg in (json_args + json_options))))
                outfile.write('{i}{i}_json_args = {{k: v for k, v in _all_json_args.items() if v != self._NO_VALUE}}\n'.format(i=indent))
                outfile.write("{i}{i}return self.connection.{method}(_api_endpoint, _json_args)\n".format(i=indent, method=method))
            else:
                outfile.write("{i}{i}return self.connection.{method}(_api_endpoint)\n".format(i=indent, method=method))
