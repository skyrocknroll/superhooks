# Superhooks

Superhooks is a supervisor "event listener" that sends events from processes that run under [supervisor](http://supervisord.org) to predefined web hooks. When `superhooks` receives an event, it sends a message notification to a configured URL.

`superhooks` uses [requests](https://2.python-requests.org/en/master/#) full-featured Python http requests library.

## Installation

```
pip install superhooks
```

## Command-Line Syntax

```bash
$ superhooks  -u http://localhost:8090/ -e STARTING,RUNNING,BACKOFF,STOPPING,FATAL,EXITED,STOPPED,UNKNOWN -d a:b::c:d -H p:q::r:s 
```

### Options

```-u URL, --url=http://localhost:8090/```

Post the payload to the url with http `POST`

```-d DATA, --data=a:b::c:d``` post body data as key value pair items are separated by `::` and key and values are separated by `:`

```-H HEADERS, --headers=p:q::r:s``` request headers with as key value pair items are separated by `::` and key and values are separated by `:`

```-e EVENTS, --event=EVENTS```

The Supervisor Process State event(s) to listen for. It can be any, one of, or all of
STARTING, RUNNING, BACKOFF, STOPPING, EXITED, STOPPED, UNKNOWN.

## Configuration
An `[eventlistener:x]` section must be placed in `supervisord.conf` in order for `superhooks` to do its work. See the “Events” chapter in the Supervisor manual for more information about event listeners.

The following example assume that `superhooks` is on your system `PATH`.

```
[eventlistener:superhooks]
command=python /usr/local/bin/superhooks -u http://localhost:8090/ -e BACKOFF,FATAL,EXITED,UNKNOWN -d a:b::c:d -H p:q::r:s
events=PROCESS_STATE,TICK_60

```


### Notes
* All the events will be buffered for 1 min and pushed to web hooks. 