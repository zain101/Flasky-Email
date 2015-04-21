#!/usr/bin/env python

import getpass, sys
from imapclient import IMAPClient

hostname = "smtp.gmail.google"
username = "eyantra226928@gmail.com"
password = "pass4eyantra"

c = IMAPClient(hostname, ssl=True)
try:
    c.login(username, getpass.getpass())
except c.Error, e:
    print 'Could not log in: ', e
    sys.exit(1)



def explore_message(c, uid):
    reply = '1.1'
    key = 'BODY[1.1]'
    try:
        msgdict = c.fetch(uid, [key])
    except c._imap.error:
        print 'Error - cannot fetch section %r' % reply
    else:
        content = msgdict[uid][key]
        if content:
            print "\n\n"
            print content
            print "\n\n"
        else:
            print '(NO such section)'


def main(c):
    c.select_folder("INBOX", raadonly=True)
    msgdict = c.fetch('1:*', ['BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)]', 'FLAGS', 'INTERNALDATE', 'RFC822.SIZE'])

    for uid in sorted(msgdict):
        items = msgdict[uid]
        print '%6d, %20s, %6d bytes %s' %  (uid, items['INTERNALDATE'], items['RFC822.SIZE'], ' '.join(items['FLAGS']))
        for i in items['BODY[HEADER.FIELDS (FROM SUBJECT)]'].splitlines():
            print ' '*6, i.strip()
    reply = raw_input('Type a message UID: ').strip()
    reply = int(reply)
    if reply in msgdict:
        explore_message(c, reply)

    c.close_folder()

if __name__ == '__main__':
    main(c)
