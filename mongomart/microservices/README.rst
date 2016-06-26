===================================
Microservices Architecture Workshop
===================================

Introduction
------------
Welcome to MongoDB Education Microservices Architecture workshop.

This document contains the requirements and set up instructions.

Requirements
------------

To run the exercises and challenges of this workshop students should have the following software setup:

- `MongoDB 3.2`_
- `Python`_
- `virtualenv`_
- `pip`_
- `Docker`_ or `Docker Machine`_

All python libraries can be found in the ``requirements.txt``

General Setup
-------------

Initialization Steps
~~~~~~~~~~~~~~~~~~~~

To initialize the environment one needs to follow these steps:

- Uncompress the workshop tarball
- Initiate a python virtual environment

.. code-block:: bash

    virtualenv venv
    source venv/bin/activate

- Install dependencies

.. code-block:: bash

    pip install -r requirements.txt

- Initialize a MongoDB instance

.. code-block:: bash

    mkdir db
    mongod --dbpath db --fork --logpath db/m.log

- Import initial dataset

.. code-block:: bash

    mongoimport -d mongomart -c item data/items.json
    mongoimport -d mongomart -c store data/stores.json
    mongoimport -d mongomart -c zip data/zips.json

Monolithic App Setup
~~~~~~~~~~~~~~~~~~~~

To boot up our test appplication we need to do the following steps:

- Start the `mongomart.py`

.. code-block:: bash

    python mongomart.py

- Students will have to:

  - Setup the connection objects
  - Some queries will be missing and they will have to figure them out
  - All application functionality should be up and running

.. solution lab-1: mc = MongoClient(); database = mc.mongomart

.. solution lab-2: cart = self.cart.find_one( { 'userid' : userid })

.. solution lab-3: pipeline = [ { "$match" : { "itemid" : itemid } },
..                 { "$group" : { "_id" : "$itemid", "avg_stars" : { "$avg" : "$stars" } } } ]

.. solution lab-4 if query == '':
..        num_items = self.item.find().count()
..    else:
..        num_items = self.item.find( { '$text' : { '$search': query } }).count()


Services
~~~~~~~~

Regarding services, we will explore different implementation options:

- Async services with Tornado
- Simple Rest interfaces using bottle
- MongoDB Rest interfaces using `Eve`_


Microservices
~~~~~~~~~~~~~




.. _`Docker Machine`: https://docs.docker.com/machine/
.. _`virtualenv`: https://virtualenv.pypa.io/en/stable/
.. _`MongoDB 3.2`: https://www.mongodb.com/download-center#community
.. _`Python`: https://www.python.org/
.. _`pip`: https://pip.pypa.io/en/stable/installing/
.. _`Eve`: http://python-eve.org/
