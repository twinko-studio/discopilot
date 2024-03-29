[![build](https://github.com/twinko-studio/discopilot/actions/workflows/build.yml/badge.svg)](https://github.com/twinko-studio/discopilot/actions/workflows/build.yml)
![PythonVersion](https://img.shields.io/badge/python-3.9%20%7C%203.8%20%7C%203.10%20%7C%203.11-blue)

# discopilot
Using discord bots to automate RSS feed processing, translation, summarization and publishing to other services such as twitter, weibo etc.


## Neo or Nexus: just give discopilot a real name [Not started yet]

The super AGI bot, the brain of the system.

Features:

- Chat bot: talk to me like my real copilot
- AI capabilities: 

Slash command central

Bot commander:

- start, stop and restart other bots, like news bot
- slash command central

Monitor:

- Monitor bot status and send alerts to monitor channel
- Monitor rate limits and send alerts to monitor channel
- Monitor social posting actions and send alerts to monitor channel

```bash
discopilot.py commander
```

## Hedwig: the message and news bot

Features:

- RSS message processing: fetch news from channels, split embedes to single messages and run filters on them
- Filtering: filter news by spam detector
- Translation: translate news to other languages and repost to language specific channels
- Summarization: summarize news by date, time, hours and daily summary and weekly summary repost to summary channel
- Publishing: publish news to other services such as twitter, weibo etc.


```bash
# start hedwig bot on discord
discopilot hedwig fly 
# start hedwig bot on discord with dev version
discopilot hedwig fly --version dev 
# fetch news from channel 1234567890 in last 24 hours
discopilot hedwig fetch --channel 1234567890 --hour 24 
# fetch news from channel 1234567890 between 2023-08-23 and 2023-08-24
discopilot hedwig fetch --channel 1234567890 --start 2023-08-23 --end 2023-08-24 
# send a message to channel 1234567890
discopilot hedwig hoot "Hello World" --channel 1234567890
# send a message to channel named monitor in config file
discopilot hedwig hoot "Hello World" --channel_name monitor
```

### Espresso: the information summarizer AI

```bash
discopilot espresso --help
# discopilot espresso "Hello, World! I am a robot, and I am here to help you."
discopilot espresso "hello world"
discopilot espresso ~/Code/twinko-studio/discopilot/tests/data/article.txt
discopilot espresso ~/report/report_20230822_204907.md 
discopilot espresso ~/Code/twinko-studio/discopilot/tests/data/article.txt --model_id sshleifer/distilbart-cnn-12-6
```

### C-3PO: the translator AI

```bash
discopilot c3po --help
discopilot c3po --list
discopilot c3po --list_target zh
discopilot c3po --detect 'Hello, World!'
discopilot c3po 'Hello, World!' --target zh
discopilot c3po 'Hello, World!' --to_zh
discopilot c3po 'Hello, World!' --target ja
```

```

### the spam detector AI

```bash

```