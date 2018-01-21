These scripts will quickly allow you to setup a single node [Kafka](http://kafka.apache.org) server using Vagrant. To get started simply:

```
$ cd apache-kafka-setup/vagrant-file
$ vagrant up
```

The Kafka server will be listening on `192.168.33.10` port `9092`.

This will take a little while to fetch and download all the required packages, etc. When it completes you should see a message like:

```
==> default: Installation complete!
```
Once you see the above message go ahead and log into the new server:

```
$ vagrant ssh

```

Once your logged in you can quickly verify Zookeeper and Kafka are running by:

```
$ ps -aux | grep java

```

Let’s create a topic. Still inside the Kafka VM run the following from the command line:

```
$ cd kafka_2.10-0.8.2.1/
$ bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
$ bin/kafka-topics.sh --list --zookeeper localhost:2181

```


