import os
import re
import sqlite3
from time import sleep

import praw
import emotes

import ponymotes


def main():

    sql = sqlite3.connect('data.db')
    cur = sql.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS comments(parsed varchar(7))")
    sql.commit()

    r = praw.Reddit()
    print('Logged in')

    mlp = r.subreddit('testingground4bots')
    comments = mlp.stream.comments()
    print('Starting comment stream')
    running = True
    while running:
        for comment in comments:

            check = cur.execute(
                "SELECT * FROM comments WHERE parsed=?", [comment.id])

            if check.fetchone() is not None:
                continue

            print('Parsing comment ' + comment.id +
                  ' by ' + comment.author.name)
            emotes = check_cond(comment)
            if emotes:
                # sleep(600)  # wait 10 minutes. dumb ratelimit
                ems = list(map(lambda e: e.name, emotes))

                print('User %s used emotes: [%s]' %
                      (comment.author.name, ', '.join(ems)))
                try_reply(comment, emotes)

            cur.execute(
                "INSERT INTO comments(parsed) VALUES (?)", [comment.id])
            sql.commit()
            if emotes:
                print('Posted! Waiting 10 minutes before posting again.')
                sleep(600)
                print('Ready to start again!')


def check_cond(comment):
    text = comment.body
    emotes = ponymotes.parse(text)
    foreign_emotes = []
    for e in emotes:
        if not e.is_default():
            foreign_emotes.append(e)
    return foreign_emotes


def try_reply(comment, foreign_motes):
    try:
        reply_ponymote(comment, foreign_motes)
    except praw.exceptions.APIException as e:
        print(e.message)
        print('Rate limit reached.')
        match = re.search(r'try again in (\d+) (minutes?|seconds?)', e.message)
        if match:
            num = match.group(1)
            unit = match.group(2)
            secs = 'second' in unit
            n = 1 if secs else 60
            wait = int(num) * n
            print('Waiting %d %s' % (wait if secs else wait / 60,
                                     'seconds' if secs else 'minutes'))
            sleep(wait)
        else:
            print('Waiting 10 minutes')
            sleep(600)
        try_reply(comment, foreign_motes)


def reply_ponymote(comment, foreign_motes):
    reply = "%sThere are some foreign emotes in your post. Be aware that not everypony\
 can see these and should be used sparingly.\n\
\nHere are the emotes that were posted.%s\n" % (
        emotes.WASNT_ME, emotes.SPACE)
    for m in foreign_motes:
        if m.nsfw:
            continue
        reply += """
[%s](%s)

- Tooltip: %s
- Flags: %s
""" % (m.name, m.view_url(), m.tooltip, "-".join(m.flags) if m.flags else None)
    reply += """
This is a bot by /u/JoyJoy_.
"""

    comment.reply(reply)


if __name__ == '__main__':
    main()
