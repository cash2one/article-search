# coding: utf-8

import logging
import Queue
import random
from contextlib import contextmanager
from elasticsearch import Elasticsearch

import common.decorator as decorator
from storage import Storage

logger = logging.getLogger(__name__)

# ElasticSearch storage
class ESStorage(Storage):
    def __init__(self, hosts, index, doc_type, doc_index, pool_size=4):
        super(ESStorage, self).__init__()
        self.hosts = hosts # ['host:port', 'host:port']
        self.es_index = index
        self.doc_type = doc_type
        self.doc_index = doc_index
        self.pool_size = pool_size
        self.client_pool = self._init_pool(pool_size)

    def _init_pool(self, size):
        try:
            pool = Queue.Queue(maxsize=size)
            for i in range(size):
                pool.put(Elasticsearch([{'host':host.split(':')[0], 'port':int(host.split(':')[1])} for host in self.hosts]))
            return pool
        except:
            raise 

    @contextmanager
    def _pick(self):
        try:
            cli = self.client_pool.get()
            #logger.debug('get es client: {cli}'.format(cli=cli))
            self.client_pool.task_done()
            yield cli
            self.client_pool.put(cli)
            #logger.debug('put es client: {cli}'.format(cli=cli))
        except:
            raise

    @decorator.trace_log(logger=logger,lvl=logging.INFO)
    def init(self):
        request_body = self.doc_index
        with self._pick() as cli:
            if not cli.indices.exists(index=self.es_index):
                logger.info('create ES index: {body}'.format(body=request_body))
                return cli.indices.create(index=self.es_index, body=request_body)
        return None

    def store(self, key, value):
        """
            index – The name of the index
            doc_type – The type of the document
            body – The document
            id – Document ID
        """
        with self._pick() as cli:
            # insert/update new record into ES
            #logger.debug('store(key={key})'.format(key=key))
            return cli.index(index=self.es_index, 
                doc_type=self.doc_type, body=value, id=key)

    @decorator.trace_log(logger=logger,lvl=logging.INFO)
    def close(self):
        count = 0
        while count < self.pool_size:
            cli = self.client_pool.get()
            self.client_pool.task_done()
            count += 1
        self.client_pool.join()
        self.pool_size = 0

