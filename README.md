# Stack Dump
Get _Links_ and **Title** from a <u>keyword</u> from Stack Exchange sites. Very useful, as it saves time. 


#### Features:

- [x] Using Stack Exchange reference through the Terminal. :computer:
- [x] Colorful CLI for catchy results from an eye :wink:


#### TODOs:
- [ ] Better exception handling.
- [ ] Local API quota calculation, for saving it.
- [ ] Multicolored requests.


#### Usage:

```
 ____  _             _      ____
/ ___|| |_ __ _  ___| | __ |  _ \ _   _ _ __ ___  _ __
\___ \| __/ _` |/ __| |/ / | | | | | | | '_ ` _ \| '_ \
 ___) | || (_| | (__|   <  | |_| | |_| | | | | | | |_) |
|____/ \__\__,_|\___|_|\_\ |____/ \__,_|_| |_| |_| .__/
                                                 |_|     v0.7
usage: stackDump.py [-h] -k KEYWORD

StackDump

optional arguments:
  -h, --help                      show this help message and exit

required arguments:
  -k KEYWORD, --keyword KEYWORD   Keyword to lookup

Example: stackdump -k "example"
```

#### Demo:

[![demo](https://asciinema.org/a/264545.svg)](https://asciinema.org/a/264545?autoplay=1)


**NOTE**: Edit code, and modify API key for more API Quota from `api_key` variable @ line 78.
