#!/usr/bin/env python3

import email
import sys
import urllib.request

msg = email.message_from_string(sys.stdin.read())
for header in msg.items():
    if header[0] == 'List-Unsubscribe':
        links = header[1].split(',')
        for link in links:
            link = link.rstrip('>')
            link = link.lstrip('<')
            if not link.startswith('https'):
                continue

            req = urllib.request.Request(link, method="POST")
            with urllib.request.urlopen(req) as response:
                print(response.read().decode('utf-8'))
                exit(0)

print('Could not unsubscribe.')
exit(1)

