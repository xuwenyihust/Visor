# Visor
Log file monitor.

 *https://xuwenyihust.github.io/Visor/*

## Log Format
### Apache Log

**Access Log**
> 127.0.0.1 user-identifier frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326

**Error Log**
> [Wed Oct 11 14:32:52 2000] [core:error] [pid 35708:tid 4328636416] [client 127.0.0.1] client denied by server configuration: /export/home/live/ap/htdocs/test

**Fields**

|Access Log Fields|Error Log Fields|
|-----|-----|
|IP address of the client|Date and time|
|RFC 1413 identity of the client|The module producing the message|
|UserID of the client|Process ID|
|Request line from the client|Client Address|
|HTTP status code|Detailed error message|
|Size of the object returned to the client||


## Configuration
Json format configuration files
**$HOME/config**
```json
{
    "heartbeat" : { 
        "interval": "3",
        "message": "HEARBEAT"
    },
    "warn": {
        "interval": {
            "min": 5,
            "max": 30
            },
        "message": [
            "Have no idea what the professor is talking about", 
            "My phone is out of battery", 
            "Forgot to bring my wallet with me", 
            "Do not play overwatch" 
        ]
    },
... ...
```

## Usage

## Example

## Requirements

## Resources
* [Apache Log Files](https://httpd.apache.org/docs/1.3/logs.html)

## License
See the LICENSE file for license rights and limitations (MIT).

