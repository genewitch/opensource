#!/usr/bin/python3

ACCESS_LOG = '~/access.log'

print("Content-Type: text/html;charset=utf-8")
print()

header = """
<html>
    <head>
        <title>Testing Python CGI</title>
    </head>
    <body>
"""

footer = """
    </body>
</html>
"""

print(header)
print('<table>')
with open(ACCESS_LOG, 'r') as log_file:
    for line in log_file:
        print('<tr><td>')
        print(line)
        print('</td</tr>')
print('</table>')
print(footer)
