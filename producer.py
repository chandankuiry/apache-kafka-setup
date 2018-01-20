#!/usr/bin/env python
# encoding: utf-8
"""
producer.py
 
"""
 
import sys
import os
import json
import uuid
import datetime
import time
import socket
import logging
import traceback
 
import confluent_kafka as kafka
 
HEADERS = {
    "avro": "application/vnd.kafka.avro.v1+json",
    "binary": "application/vnd.kafka.binary.v1+json",
    "json": "application/vnd.kafka.json.v1+json"
}
 
def _printer(err, msg):
    """Test callback for producer"""
     
    print
    if not err:
        print "Produced message and received: [{}]".format(msg.value().encode('utf-8'))
    else:
        print "Received error sending message [{}] with msg [{}]".format(err, msg.value().encode('utf-8'))
 
 
class StreamProducer:
     
    def __init__(self, cfg):
        self.config = cfg
        self.producer = None
         
 
    # create logger
    def __get_logger(self):
        """Instantiates logger."""
        return logging.getLogger(os.path.basename(__file__))
     
     
    def _get_connection(self):
        """Returns producer object"""
         
        logger = self.__get_logger()
                     
        try:
            conf = {'bootstrap.servers': ','.join(map(str, self.config.get('hosts'))),
                'client.id': socket.gethostname(),
                'default.topic.config': {'acks': 'all'}
            }
             
            producer = kafka.Producer(**conf)
            self.producer = producer # set class level for reuse
             
        except Exception, e:
            logger.error( "Error establishing Kafka producer" )
            logger.debug( traceback.format_exc() )
            raise kafka.KafkaException(e)
         
 
    def publish(self, data, topic='test', key=None, partition=None, callback=None):
        """POSTs data to Kafka REST proxy"""
     
        logger = self.__get_logger()
     
        try:
            if self.producer is None:
                self._get_connection()
            # end if producer
             
            logger.debug( "Sending message to topic [{}] with key [{}]".format(topic, key) )
             
            self.producer.produce(
                topic, 
                json.dumps(data, separators=(',', ':')).encode('utf-8'), 
                key=key, 
                on_delivery=callback
            )
            #self.producer.flush()
             
        except Exception, e:
            logger.error( "Error publishing data" )
            logger.debug( traceback.format_exc() )
 
     
 
def main():
     
    logging.basicConfig(level=logging.DEBUG)
     
    cnf = {
        "hosts": ["localhost:9092"]
    }
     
    s = StreamProducer(cnf)
     
    data = {"id": str(uuid.uuid1()), "some data": "some value", "some more data": "another value"}
     
    s.publish(data, topic='test', key='12345', callback=_printer)
 
 
 
 
if __name__ == '__main__':
    main()