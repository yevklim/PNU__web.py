#!/usr/bin/python

import cgi
import sys
from os import environ
from http.cookies import SimpleCookie

form = cgi.FieldStorage()

author = form.getfirst("author", None)
song = form.getfirst("song", None)
song_format = form.getfirst("songFormat", "mp3")
include_cover_image = form.getfirst("includeCoverImage", False)
include_other_metadata = form.getfirst("includeOtherMetadata", False)

found_song = author and song

cookie = SimpleCookie(environ.get("HTTP_COOKIE"))
counter = cookie.get("counter")
if counter is None:
    counter = 0
else:
    try:
        counter = int(counter.value)
    except:
        counter = 0
new_counter = counter + 1

print(f"Set-cookie: counter={new_counter};")

print("Content-type:text/html\r\n\r\n")

if (found_song):
    print(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>{song} - {new_counter}</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"
                integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous" />
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
                integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL"
                crossorigin="anonymous"></script>
        </head>
        <body class="container my-4">
            <p class="h1">Song "{song}" by "{author}"</p>
            <p>* available in {song_format} format</p>
            <p>* {"includes" if include_cover_image else "doesn't include"} cover image</p>
            <p>* {"includes" if include_other_metadata else "doesn't include"} full metadata</p>
            <p>
            <mark>
                <a href="javascript:alert('What did you expect, huh?')">Download your #{new_counter} song</a>
            </mark>
            </p>
        </body>
        </html>
    """)
else:
    print(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>404 Not Found</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"
                integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous" />
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
                integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL"
                crossorigin="anonymous"></script>
        </head>
        <body class="container my-4">
            <p class="h1">Requested song was not found</p>
        </body>
        </html>
    """)
