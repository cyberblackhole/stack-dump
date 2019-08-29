# Stack Dump
Information Gathering tool to get _Links_ and **Title** from Stack Exchange sites for a specific <u>keyword</u>. 


#### Features:

- [x] Using Stack Exchange Advanced Search through the Terminal. :computer:
- [x] Colorful CLI for catchy results :wink:


#### TODOs:
- [ ] Writing output to different file formats


#### Usage:

```
 ____  _             _      ____
/ ___|| |_ __ _  ___| | __ |  _ \ _   _ _ __ ___  _ __
\___ \| __/ _` |/ __| |/ / | | | | | | | '_ ` _ \| '_ \
 ___) | || (_| | (__|   <  | |_| | |_| | | | | | | |_) |
|____/ \__\__,_|\___|_|\_\ |____/ \__,_|_| |_| |_| .__/
                                                 |_|     v0.7
usage: stackDump.py [-h] -k KEYWORD [-l LIMIT]

StackDump

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -k KEYWORD, --keyword KEYWORD
                        Keyword to lookup
  -l LIMIT, --limit LIMIT
                        Limit Results per Stack Site: min:10

Example: stackdump -k "example"
```

#### Demo:

[![Demo](https://asciinema.org/a/264650.svg)](https://asciinema.org/a/264650?autoplay=1)
