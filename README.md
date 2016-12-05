# Visor
Log file monitor.

 *https://xuwenyihust.github.io/Visor/*

## Log Format
### Apache Log

**Access Log**
> 127.0.0.1 user-identifier frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326

**Error Log**
> [Wed Oct 11 14:32:52 2000] [error] [client 127.0.0.1] client denied by server configuration: /export/home/live/ap/htdocs/test

**Fields**

|Access Log Fields|Error Log Fields|
|-----|-----|
|IP address of the client|Date and time|
|RFC 1413 identity of the client|The module producing the message|
|UserID of the client|Process ID|
|Request line from the client|Client Address|
|HTTP status code|Detailed error message|
|Size of the object returned to the client||


## Usage

## Example

## Requirements

## Resources

## License
See the LICENSE file for license rights and limitations (MIT).

