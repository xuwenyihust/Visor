![Python 3.4](https://img.shields.io/badge/python-3.4-green.svg)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/xuwenyihust/Visor/blob/master/LICENSE)
[![in progress](https://img.shields.io/badge/in%20progress-3-orange.svg)](https://github.com/xuwenyihust/Visor/projects/1)

<img src="https://raw.githubusercontent.com/xuwenyihust/Visor/master/img/Visor.JPG" align="right" />
# Visor: Real-time Log Monitor - [Read The Docs](https://goo.gl/F0rADZ)

Web page: *https://xuwenyihust.github.io/Visor/*

Visor is a real-time log monitor that supports different log patterns, currently Apache access log format and Apache error log format.

Visor can monitor multiple log sources at the same time, and in realtime with the help of Apache Kafka and Spark Streaming.

This can be a simple and relative complete example of real-time log monitor, if you have a lot of continously generated logs to be analyzed, or you want to learn how to build a log monitor, Visor can be a good choice.

Also, if you want to see how Visor works, or have your own monitor to test, but you don't have access to real logs, Visor has its own fake log generator to generate likely log files for analytics.

## Documentation
The Visor's documentation is hosted on GitBook at https://xuwenyihust.gitbooks.io/visor-real-time-log-monitor/content/. 

## Overview
Visor is designed to be highly modular. Easly to be configured, and extended if you want. 

The whole platform is composed of several components: 
* Fake log generator
* Log import system
* Log analysis system
* Alerting system
* Output Storage
* Dashboard

### Fake Log Generator

Currently we support generating and analyzing 2 log formats: Apache access log format and Apache error log format.

|Access Log Fields|Error Log Fields|
|-----|-----|
|IP address of the client|Date and time|
|RFC 1413 identity of the client|Message level|
|UserID of the client|Process ID|
|The time that the request was received|Client Address|
|Request line from the client|Detailed error message|
|HTTP status code|N/A|
|Size of the object returned to the client|N/A|

The generated log lines will be stored into files by default, you can also stream them into the analysis part through TCP sockets or Apache Kafka.

### Log Import
Support 3 log import modes:
* Direct file import
* TCP socket transmission
* Apache Kafka streaming

### Log Analysis
The platform also provides 3 different analysis application:
* Mini-monitor
* Spark-monitor

The mini-monitor is a simple prototype, written in pure Python. It can only work with the direct file import method, and write the analysis results into a file.

The application implemented with Spark Streaming can realize real-time when used with Apache Kafka.

## Configuration
### Environment Variables
Add the application's root directory to both `$PYTHONPATH` and `$VISORHOME`.

### Configuration Files
Use JSON for configuration files, all stored under **$HOME/config**. 

An example of the configuration files:
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

### Direct File Import + Mini-Monitor

* Run fake log generator:

```
python3.4 $VISORHOME/src/fake_log_gen/fake_log_gen.py -m [access/error] -o [logfile]
```

* Run Mini-Monitor to analyze generated log files:
```
python3.4 $VISORHOME/src/mini_monitor/mini_monitor.py -i [logfile]
```

### TCP Transmission + Spark Streaming

* Generate fake logs and run as TCP server:

```
python3.4 $VISORHOME/src/socket/fake_log_stream.py -m [access/error]
```

* Run Spark Streaming application to receive & analyze logs

```
$SPARK_HOME/bin/spark-submit $VISORHOME/src/stream_monitor/stream_monitor.py
```

### Kafka Streaming + Spark Streaming
* Start a Kafka server:
```
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties
```

* Create a Kafka topic:
```
$KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
```

* Generate fake logs and run as Kafka producer:
```
python3.4 $VISORHOME/src/fake_log_gen/fake_log_producer.py -m [access/error]
```

* Run Spark Streaming application to consume & analyze logs
```
$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 $VISORHOME/src/kafka_monitor/kafka_monitor.py
```


## Resources
* [Apache Log Files](https://httpd.apache.org/docs/1.3/logs.html)
* [Unit Testing TCP Server & Client with Python](http://www.devdungeon.com/content/unit-testing-tcp-server-client-python)

## License
See the LICENSE file for license rights and limitations (MIT).

