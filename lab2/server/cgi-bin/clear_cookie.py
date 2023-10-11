#!/usr/bin/python

print(f"Set-cookie: counter=;")
print("Content-type:text/html\r\n\r\n")

print("<script>location.assign(\"/\")</script>")
