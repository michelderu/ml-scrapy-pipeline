# -*- coding: utf-8 -*-
  
# MarkLogic Pipeline for Scrapy
#
# Uses the MarkLogic REST document endpoint to load scraped items.
#
# Takes configuration from settings.py in the form of:
# ITEM_PIPELINES = {
#    'recall.pipelines.MarkLogicPipeline': 300,
# }
#
# MARKLOGIC_DOC_ENDPOINT = 'http://localhost:8000/v1/documents'
# MARKLOGIC_USER = 'admin'
# MARKLOGIC_PASSWORD = 'admin'
# MARKLOGIC_CONTENT_TYPE = 'xml'
# MARKLOGIC_COLLECTIONS = ['data', 'data/events']
# MARKLOGIC_TRANSFORM = ''
#
# If json output is preferred, use MARKLOGIC_CONTENT_TYPE = 'json'.
# In case MARKLOGIC_COLLECTIONS = '', the spider_name will be used for the collection.
#
# In items.py:
# The only the field 'uri' is required as it is used for URI of the document in MarkLogic.
#
  
import dicttoxml
import json
import logging
import re
import requests
from tidylib import tidy_document
from requests.auth import HTTPDigestAuth
from dicttoxml import dicttoxml
  
class MarkLogicPipeline(object):
  
    def __init__(self, ml_uri, ml_user, ml_pwd, ml_content, ml_transform, ml_collections):
        self.ml_uri = ml_uri
        self.ml_user = ml_user
        self.ml_pwd = ml_pwd
        self.ml_content = ml_content
        self.ml_collections = ml_collections        
        self.ml_transform = ml_transform
  
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            ml_uri = crawler.settings.get('MARKLOGIC_DOC_ENDPOINT'),
            ml_user = crawler.settings.get('MARKLOGIC_USER'),
            ml_pwd = crawler.settings.get('MARKLOGIC_PASSWORD'),
            ml_content = crawler.settings.get('MARKLOGIC_CONTENT_TYPE'),
            ml_collections = crawler.settings.get('MARKLOGIC_COLLECTIONS'),
            ml_transform = crawler.settings.get('MARKLOGIC_TRANSFORM')
        )
  
    def process_item(self, item, spider):
        if (self.ml_content == 'xml'):
            self.marklogic_put_xml (item, spider.name)
        elif (self.ml_content == 'json'):
            self.marklogic_put_json (item, spider.name)
  
        return item
  
    def marklogic_put_xml(self, item, spider_name):
        # Set the uri and collection
        if (self.ml_transform == ''):
            params = {'uri': item['uri'], 'collection': self.ml_collections or spider_name}
        else:
            params = {'uri': item['uri'], 'collection': self.ml_collections or spider_name, 'transform': self.ml_transform}
        # Set up the XML payload
        payload = dicttoxml(dict(item), attr_type=False, custom_root='webcontent')
        # Decode the <> characters back again
        payload = payload.replace('&lt;', '<').replace('&gt;', '>').replace('&apos;', "'").replace('&quot;', '"')
        # Run tidy in order to get wel-formed XML
        payload, errors = tidy_document(payload, options={'input-xml': 1})
  
        # Set up the header
        headers = {'Content-Type': 'application/xml'}
  
        ml_uri = ('ml_uri' in item and item['ml_uri']) or self.ml_uri
        logging.info("PUTting XML in " + ml_uri + " as " + item['uri'])
  
        # Call the MarkLogic REST endpoint
        ml_user = ('ml_user' in item and item['ml_user']) or self.ml_user
        ml_pwd = ('ml_pwd' in item and item['ml_pwd']) or self.ml_pwd
        r = requests.put(ml_uri,
            params = params,
            auth = HTTPDigestAuth(ml_user, ml_pwd),
            data = payload,
            headers = headers)
  
        logging.info("PUT response: " + str(r.status_code) + ", " + r.text)
  
    def marklogic_put_json(self, item, spider_name):
        # Set the uri and collection
        params = {'uri': item['uri'], 'collection': self.ml_collections or spider_name}
        # Set up the JSON payload
        payload = json.dumps(dict(item))
        # Set up the header
        headers = {'Content-Type': 'application/json'}
  
        ml_uri = ('ml_uri' in item and item['ml_uri']) or self.ml_uri
        logging.info("PUTting JSON in " + ml_uri + " as " + item['uri'])
  
        # Call the MarkLogic REST endpoint
        ml_user = ('ml_user' in item and item['ml_user']) or self.ml_user
        ml_pwd = ('ml_pwd' in item and item['ml_pwd']) or self.ml_pwd
        r = requests.put(ml_uri,
            params = params,
            auth = HTTPDigestAuth(ml_user, ml_pwd),
            data = payload,
            headers = headers)
  
        logging.info("PUT response: " + str(r.status_code) + ", " + r.text)
