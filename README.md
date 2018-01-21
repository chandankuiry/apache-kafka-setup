### What is kafka
Kafka is an opensource distributed streaming platform  that simplifies data integration between systems.
A stream is a pipeline to which your applications receives data continously.
As a streaming platform kafka has two primary uses:
* Data Integration: Kafka captures streams of events or data changes and feeds these to other data systems such as relational databases, key-value stores or  data warehouses.
* Stream processing: Kafka accepts each stream of event and stores it in an append only queue  called a log.Information in the log is immutable hence enables continuous, real-time processing and transformation of these streams and makes the results available system-wide.

Compared to other technologies, Kafka has a better throughput, built-in partitioning, replication, and fault-tolerance which makes it a good solution for large scale message processing applications.

Kafka system has three main components:
1. A Producer:  The service which produces the data that needs to be broadcast
2. A Broker:  This is Kafka itself , which acts as a middle man between the producer and the consumer. It utilises the power of API's to get and broadcast data
3. A Consumer: The service that utilises the data which the broker will broadcast.



## Installing Kafka


- for linux user follow installation instruction from [here](https://www.tutorialspoint.com/apache_kafka/apache_kafka_installation_steps.htm)
- By default Kafka runs on port `9092`

-otherwise for vagrant setup click [here](https://github.com/chandankuiry/apache-kafka-setup/tree/master/vagrant-file) 
-If you install kafka using vagrant then Kafka server will be listening on `192.168.33.10` port `9092`.