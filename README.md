# Superhooks

Superhooks is a supervisor "event listener" that sends events from processes that run under [supervisor](http://supervisord.org) to predefined web hooks. When `superhooks` receives an event, it sends a message notification to a configured URL.

`superhooks` uses [requests](https://2.python-requests.org/en/master/#) full-featured Python http requests library.

## Installation

```
pip install superhooks
```

## Command-Line Syntax

```bash
$ superhooks  -u http://localhost:8090/ -e STARTING,RUNNING,BACKOFF,STOPPING,FATAL,EXITED,STOPPED,UNKNOWN -d "a^b^^c^d" -H "p^q^^r^s" 
# Telegram Example
$ superhooks  -u https://api.telegram.org/bot$YOURBOT/sendMessage -d "chat_id^$YOURID^^text^dump_params^^disable_notifications^true" -e  STARTING, RUNNING, BACKOFF, STOPPING, EXITED, STOPPED, UNKNOWN
```

### Options

```-u URL, --url=http://localhost:8090/```

Post the payload to the url with http `POST`

```-d DATA, --data=a^b^^c^d``` post body data as key value pair items are separated by `^^` and key and values are separated by `^`, if `dump_params` is used as value `foo:dump_params` foo will dump `eventname` and all params

```-H HEADERS, --headers=p^q^^r^s``` request headers with as key value pair items are separated by `^^` and key and values are separated by `^`

```-e EVENTS, --event=EVENTS```

The Supervisor Process State event(s) to listen for. It can be any, one of, or all of STARTING, RUNNING, BACKOFF, STOPPING, EXITED, STOPPED, UNKNOWN.

## Configuration
An `[eventlistener:x]` section must be placed in `supervisord.conf` in order for `superhooks` to do its work. See the “Events” chapter in the Supervisor manual for more information about event listeners.

The following example assume that `superhooks` is on your system `PATH`.

```
[eventlistener:superhooks]
command=python /usr/local/bin/superhooks -u http://localhost:8090/ -e BACKOFF,FATAL,EXITED,UNKNOWN -d "a^b^^c^d" -H "p^q^^r^s"
events=PROCESS_STATE,TICK_60

```
### The above configuration  will produce following payload for an crashing process named envoy

```
POST / HTTP/1.1
Host: localhost:8090
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 177
Content-Type: application/x-www-form-urlencoded
P: q
R: s
User-Agent: python-requests/2.12.1

from_state=RUNNING&a=b&c=d&event_name=PROCESS_STATE_EXITED&process_name=cat%3Ameow&pheaders_all=from_state%3ARUNNING+processname%3Ameow+pid%3A25232+expected%3A0+groupname%3Acat+
```

### Notes
* All the events will be buffered for 1 min and pushed to web hooks. 

### Development 
* Modify the changes.
* Execute `python setup.py publish` 
