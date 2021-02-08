# OAI_harvester
The present OAI harvester is an implementation of a harvester to collect iconographic material from the [Online Catalogue](http://foto.biblhertz.it/exist/foto/search.html) of the [Photographic Collection](https://www.biblhertz.it/en/photographic-collection) (Fototeca) at [the Max-Planck Center for the History of Art and Architecture – Bibliotheca Hertziana](https://www.biblhertz.it/en/home) (Biblhertz). 

The repository contains the following files:

* _requirements.txt_ All the required modules that have to be installed in order to run _Biblhertz_OAI_harvester.ipynb_. Please run `pip install -r requirements.txt`
* _Biblhertz_IMG_harvester.py_ A python script of an image harvester. The latter is based on the database collected with the _Biblhertz_OAI_harvester.py_. In order to run the script, the nature of the images to be downloaded has to be specified. The script takes the following parameters:
```python
--type [Zeichnung Text Ort ...]
--artist [Caravaggio Bernini ...]
--title []
--date_begin [1560]
--date_end [1760]
--medium [Marmor Öl Papier ...]
--all [True | False]
```
* _Biblhertz_OAI_harvester.py_ A python script version of an OAI harvester which queries the [https://oai.biblhertz.it/foto/oai-pmh] url, retrieves all the objects with identifiers '08######' and stores their corresponding information in a _biblhertz.db_ database. To run on a terminal `python Biblhertz_OAI_harvester.py`
* _Biblhertz_OAI_harvester.ipynb_ A python notebook version of an OAI harvester which queries the [https://oai.biblhertz.it/foto/oai-pmh] url, retrieves all the objects with identifiers '08######' and stores their corresponding information in a _biblhertz.db_ database
* _Biblhertz_foto_retrieval.ipynb_ A first draft to collect digital images based on a local .xml file of the online database. __Will be deleted soon__

## How to use the harvester
First run _Biblhertz_OAI_harvester.py_ in your terminal. The database _biblhertz.db_ will be created in your current folder.
Then, if you want to collect images on top of the metadata, run the _Biblhertz_OAI_harvester.py_ script. A folder called _biblhertz_images_ will be created in your current directory.
`python Biblhertz_OAI_harvester.py`
`python Biblhertz_IMG_harvester.py --type Zeichnung Malerei --date_begin 1560`

## TODO
- [x] Get all objects information from the Fototeca of the Bibliotheca Hertziana
- [x] Create a .py version of the harvester to run on command line
- [x] Get digital images from specific types or all data collected with _Biblhertz_OAI_harvester.ipynb_

## Specific Documentation

The Fototeca provides [documentation](https://github.com/hertzphoto/RomaFototeca/tree/master/documentation) about its OAI system on its [GitHub account 'hertzphoto'](https://github.com/hertzphoto/RomaFototeca): 
* [Identifiers[(https://github.com/hertzphoto/RomaFototeca/blob/master/documentation/identifiers.md)
* [Mapping notes](https://github.com/hertzphoto/RomaFototeca/blob/master/documentation/mapping-notes.md)
* [OAI Repository](https://github.com/hertzphoto/RomaFototeca/blob/master/documentation/oai-pmh.md)
* [Query parameters](https://github.com/hertzphoto/RomaFototeca/blob/master/documentation/query-parameters.md)

The data in the Online catalogue is organized according to the [Marburger Informations-, Dokumentations-, und Adminisstrations-System (MIDAS)](http://archiv.ub.uni-heidelberg.de/artdok/3770/) (Bove, Heusigner and Kailus. 2001).

## Reference project:

The Städel Museum provides [best-practice documentation](https://sammlung.staedelmuseum.de/en/oai/guide) about their [OAI interface](https://sammlung.staedelmuseum.de/api/oai?verb=Identify)

The Fondazione Federico Zeri – Università di Bologna provides a good example of [query system on through as web app](http://data.fondazionezeri.unibo.it/query/)
