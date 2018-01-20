#!/usr/bin/env python
# encoding: utf-8
"""
consumer.py
"""
 
import sys
import os
import json
import uuid
import datetime
import time
import logging
import traceback
import confluent_kafka as kafka
 
 
def _printer(msg):
    """Test function to print messages from consumer"""
 
    print
    print("%s:%d:%d: key=%s value=%r" % (msg.topic(), msg.partition(),
                                         msg.offset(), msg.key(), msg.value().decode('utf-8')))
 
def _on_assign (c, ps):
    """Resets the consumer offset"""
    for p in ps:
        p.offset=-2
    c.assign(ps)
                                                                                  
 
class StreamConsumer:
     
    def __init__(self, cfg, group_id=None):
        self.config = cfg
        self.group_id = group_id
        self.consumer = None
 
 
    # create logger
    def __get_logger(self):
        """Instantiates logger."""
        return logging.getLogger(os.path.basename(__file__))
 
 
    def consume(self, topics, auto_offset='latest', processor=_printer, *args):
        """Connects to topic and listens for messages, handing them off to processor"""
 
        logger = self.__get_logger()
 
        try: 
            running = True
             
            conf = {
                'bootstrap.servers': ','.join(map(str, self.config.get('hosts'))),
                'group.id': self.group_id,
                'default.topic.config': {'auto.offset.reset': auto_offset}
            }
 
            try:
                c = kafka.Consumer(**conf)
            except:
                logger.error( "Error creating Consumer with config [{}]".format(conf) )
 
            try:
                if auto_offset == 'earliest' or auto_offset == 'smallest':
                    c.subscribe(topics, on_assign=_on_assign)
                else:
                    c.subscribe(topics)
            except:
                logger.error( "Error subscribing to topics [{}]".format(topics) )
                c = None
 
            if c:
                logger.info( "Starting to poll topics [{}]...".format(topics) )
                while running:
                    try:
                        msg = c.poll()
                        if not msg.error():
                            processor(msg)
                        elif msg.error().code() == kafka.KafkaError._PARTITION_EOF:
                            # End of partition event
                            logger.debug( "{} [{}] reached end at offset {}".format(
                                            msg.topic(), msg.partition(), msg.offset()) )
                        else:
                            logger.debug( "Unknown error [{}]. Quitting...".format(msg.error()) )
                            raise kafka.KafkaException(msg.error())
                    except:
                        running = False
                        logger.error( "Error polling messages." )
                # end while running loop
            else:
                logger.error( "Consumer object missing. Nothing to do!" )
 
            try:
                c.close() # close connection
            except:
                logger.warn( "Could not close connection (c). Nothing to do!" )
 
        except Exception, e:
            logger.error( "Error consuming topics [{}]".format(topics) )
            logger.debug( traceback.format_exc() )
 
        return None
 
 
 
def main():
     
    logging.basicConfig(level=logging.DEBUG)
     
    cnf = {
        "hosts": ["192.168.33.10:9092"]
    }
     
    c = StreamConsumer(cnf, group_id='testgroup')
     
    topics_list = ['test', 'test1', 'test2']
     
    c.consume(topics_list,
              auto_offset='smallest')
 
 
if __name__ == '__main__':
    main()