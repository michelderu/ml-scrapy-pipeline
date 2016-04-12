# MarkLogic Pipeline for Scrapy
This Scrapy Pipeline makes it easy to ingest scraped content from websites directly into MarkLogic as XML or JSON. Thereby enabling you to define the content's collections. Also it allows you to define a transform.

## How it works
Uses the MarkLogic REST document endpoint to load scraped items.

## How to configure
Takes configuration from settings.py in the form of:

ITEM_PIPELINES = {  
	'recall.pipelines.MarkLogicPipeline': 300,  
	}  
MARKLOGIC_DOC_ENDPOINT = 'http://localhost:8000/v1/documents'  
MARKLOGIC_USER = 'admin'  
MARKLOGIC_PASSWORD = 'admin'  
MARKLOGIC_CONTENT_TYPE = 'xml'  
MARKLOGIC_COLLECTIONS = ['data', 'data/events']  
MARKLOGIC_TRANSFORM = ''  

In items.py:
The only the field 'uri' is required as it is used for URI of the document in MarkLogic.

## Further configuration options
If json output is preferred, use MARKLOGIC_CONTENT_TYPE = 'json'.
In case MARKLOGIC_COLLECTIONS = '', the spider_name will be used for the collection.
