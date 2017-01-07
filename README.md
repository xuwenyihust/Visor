![Python 3.4](https://img.shields.io/badge/python-3.4-green.svg)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)]()
[![in progress](https://img.shields.io/badge/in%20progress-3-orange.svg)](https://github.com/xuwenyihust/Visor/projects/1)

<img src="https://raw.githubusercontent.com/xuwenyihust/Visor/master/img/Visor.JPG" align="right" />
# Visor: Real-time Log Monitor - [Docs](https://goo.gl/F0rADZ)

Web page: *https://xuwenyihust.github.io/Visor/*

Visor is a real-time log monitor that support different log patterns, currently Apache access log format and Apache error log format.

Visor can monitor multiple log sources at the same time, and in realtime with the help of Apache Kafka and Spark Streaming.

This can be a simple and relative complete example of real-time log monitor, if you have a lot of continously generated logs to be analyzed, or you want to learn how to build a log monitor, Visor can be a good choice.

Also, if you want to see how Visor works, or have your own monitor to test, but you don't have access to real logs, Visor has its own fake log generator to generate likely log files for analytics.

## Documentation
The Visor's documentation is hosted on GitBook at https://xuwenyihust.gitbooks.io/visor-real-time-log-monitor/content/. 

## Overview
### Log Format

|Access Log Fields|Error Log Fields|
|-----|-----|
|IP address of the client|Date and time|
|RFC 1413 identity of the client|Message level|
|UserID of the client|Process ID|
|The time that the request was received|Client Address|
|Request line from the client|Detailed error message|
|HTTP status code|N/A|
|Size of the object returned to the client|N/A|

### Data Import
Support 3 data import modes:
* Direct file import
* TCP socket transmission
* Apache Kafka streaming

### Data Analysis
The platform offers 2 different analysis application:
* Mini-monitor:		Pure Python, simple prototype, used with direct file import method
* Spark Streaming:	Realize real-time when used with Apache Kafka

## Configuration
### $PYTHONHOME
Add the root directory to `$PYTHONHOME`.

### Configuration Files
Use JSON for configuration files, stored at **$HOME/config**. Here are part of the configurations.
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
    }
```

## Usage

### Log Generation

**Apache Access Log**
```
python3.4 ../src/fake_log_gen/fake_log_gen.py fake_access_file.log access
```

**Apache Error Log**
```
python3.4 ../src/fake_log_gen/fake_log_gen.py fake_error_file.log error
```

## Requirements
* Python 3.4

## Resources
* [Apache Log Files](https://httpd.apache.org/docs/1.3/logs.html)

## License
See the LICENSE file for license rights and limitations (MIT).

