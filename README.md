[![Python](https://img.shields.io/badge/python-3.4%2C%203.5%2C%203.6-blue.svg)](https://travis-ci.org/xuwenyihust/Visor)
[![release](https://img.shields.io/badge/release-v0.0-orange.svg)](https://github.com/xuwenyihust/Visor/releases/tag/v0.0)
[![Travis](https://travis-ci.org/xuwenyihust/Visor.svg?branch=master)](https://travis-ci.org/xuwenyihust/Visor)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/xuwenyihust/Visor/blob/master/LICENSE)
[![Coverage Status](https://coveralls.io/repos/github/xuwenyihust/Visor/badge.svg)](https://coveralls.io/github/xuwenyihust/Visor)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/xuwenyihust/Visor.svg)](http://isitmaintained.com/project/xuwenyihust/Visor "Percentage of issues still open")

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

The generated log lines will be stored into files by default, you can also stream them into the analysis part through TCP sockets or Apache Kafka.

#### Log Format

  Currently we support generating and analyzing 2 [log formats](https://github.com/xuwenyihust/Visor/wiki/Log-Formats): Apache access log format and Apache error log format.

|Access Log Fields|Error Log Fields|
|-----|-----|
|IP address of the client|Date and time|
|RFC 1413 identity of the client|Message level|
|UserID of the client|Process ID|
|The time that the request was received|Client Address|
|Request line from the client|Detailed error message|
|HTTP status code|N/A|
|Size of the object returned to the client|N/A|


#### Log Traffic Control

In real world, log traffic may have huge **peaks**, and these peaks may lead to high latencies in our streaming system. 

So the generator supports suddenly producing huge amounts of logs in a short time to try to give the streaming system more pressures.

* **Log import rates shown by Spark UI:** (*with backpressure off*)

  <img src="https://github.com/xuwenyihust/Visor/blob/master/img/fake_log_peak.JPG" />

#### Log Content Control

The generator supports controlling the log fields contents, such as HTTP status code in access logs and client address in error logs.

* **Client address distribution:** (*binomial distribution*)

  Initialize a pool of client addresses, then generate the index to the pool applying binomial distribution every time to select address for a error log line.

  <img src="https://github.com/xuwenyihust/Visor/blob/master/img/fake_log_ip_dist.JPG" />

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

### Alert System
The alert system can detect & announce errors with very short latency.

### Architecture

Kafka + Spark Streaming:

<img src="https://raw.githubusercontent.com/xuwenyihust/Visor/master/img/visor_architecture.JPG" align="middle" />

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

### Alert / Report Sender Email

A new json file needs to be created by user to store the authentication information of the Alert / Report system sender email.

The format should be like:

```json
{
	"email": {
		"address": "XXXXXXXXXXXXX",
		"password": "XXXXXXXXXXXXX"
	}
}

```
And named after 'private.json'.

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
$KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic Logs
```

* Check if the topic has been created:
```
$KAFKA_HOME/bin/kafka-topics.sh --list --zookeeper localhost:2181
```

```
>>> Output:

...
Logs
...
```

* Generate fake logs and run as Kafka producer:
```
python3.4 $VISORHOME/src/fake_log_gen/fake_log_producer.py -m [access/error] -o $VISORHOME/log/fake_log_producer.log
```

* Run Spark Streaming application to consume & analyze logs
```
$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 $VISORHOME/src/kafka_monitor/kafka_monitor.py > $VISORHOME/log/kafka_monitor.log
```

## Environment

Check the [Visor's Wiki](https://github.com/xuwenyihust/Visor/wiki/Environment) to see the test environment.

## Performance

|Spec|Stat|
|------|------|
|Batch Interval|3 Sec|
|# of Executors|1|
|# of Cores per Executor|4|
|# of Kafka Tpoic Partition|1|
|Avg Input Rate|41.76 Rec/Sec|
|Avg Processing Time|2 Sec 256ms|


## Resources
* [Apache Log Files](https://httpd.apache.org/docs/1.3/logs.html)
* [Unit Testing TCP Server & Client with Python](http://www.devdungeon.com/content/unit-testing-tcp-server-client-python)
* [How to choose the number of topicspartitions in a kafka cluster](https://www.confluent.io/blog/how-to-choose-the-number-of-topicspartitions-in-a-kafka-cluster/)

## License
See the LICENSE file for license rights and limitations (MIT).

