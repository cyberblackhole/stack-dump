# Stack Dump
Information Gathering tool to get _Links_ and **Title** from Stack Exchange sites for a specific <u>keyword</u>. 


#### Features:

- [x] Using Stack Exchange Advanced Search through the Terminal. :computer:
- [x] Search for an answer posted by a particular user
- [x] Search for a question posted by a particular user
- [x] Search for a comment posted by a particular user
- [x] Colorful CLI for catchy results :wink:


#### TODOs:
- [ ] Writing output to different file formats
- [ ] Optimization and better code


#### Usage:

```
 ____  _             _      ____
/ ___|| |_ __ _  ___| | __ |  _ \ _   _ _ __ ___  _ __
\___ \| __/ _` |/ __| |/ / | | | | | | | '_ ` _ \| '_ \
 ___) | || (_| | (__|   <  | |_| | |_| | | | | | | |_) |
|____/ \__\__,_|\___|_|\_\ |____/ \__,_|_| |_| |_| .__/
                                                 |_|     v0.7
usage: stackDump.py [-h] [-k KEYWORD] [-l LIMIT] [-f USER] [-e] [-u USERID]
                    [-t TYPE]

StackDump

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -k KEYWORD, --keyword KEYWORD
                        Keyword to lookup
  -l LIMIT, --limit LIMIT
                        Limit Results per Stack Site: min:10
  -f USER, --find-user USER
                        UserId Lookup by Keyword
  -e, --exact-match     Case sensitive search
  -u USERID, --user-id USERID
                        Stack UserId got from -f/--find-user
  -t TYPE, --type TYPE  Get all answers, questions and comments posted by an UserId

Example:
 
            Advanced Keyword Search: stackdump -k "example"

            Keywork search with Limit: stackdump -k "example" -l 50

            Find User exact match: stackdump -f Goron -e

            Get answers for Userid: stackdump -u 123123 -t answers

            Get questions for Userid: stackdump -u 123123 -t questions

            Get comments for Userid: stackdump -u 123123 -t comments

```

#### Demo:

[![Demo](https://asciinema.org/a/264650.svg)](https://asciinema.org/a/264650?autoplay=1)
