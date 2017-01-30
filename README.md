# makerestapiclient
Simple python tool to build a REST API client from a json description file (or
any other list of endpoints).

## I wouldn't recommend using this project.  It works, and it's useable, but you're probably much better off using the OpenAPI specification to generate a client library.  [swagger-codegen](https://github.com/swagger-api/swagger-codegen) is one such project.

# Install

Like most packages, you can install this one by name:

    sudo pip3 install makerestapiclient

# Use

Most of it is specified by the json API.  Other than your HTTP handler, almost
The function name is derived from "name", or "endpoint" if the name is not
all of it should be able to be generated automatically.
available. endpoint is specified as an "endpoint", "data-args" are mandatory
data arguments, "data-options" are optional data arguments (it's up to your HTTP
handler to encode and send these).  "query-args" and "query-options" are the
same, but for Query data on the URL.  "description" is embedded as a doc
string.  "defaults" should map default arguments for the function.

A default HTTP handler can be found in http.py here.  I would not recommend
referencing it directly as makerestapiclient.http.HTTP, but rather copying it
into your own project if you need it, as it's silly to require this module for
a simple example file.

Depending how this is called, it can also build out context managers for your
use.
