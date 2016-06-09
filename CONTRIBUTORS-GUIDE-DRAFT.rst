==================
Contributers Guide
==================


Source
------

The source for the curriculum in this repository is found in the `source`_ subdirectory. We model curriculum as follows:

- modules (e.g., compound indexes)
- examples
- exercises
- figures or images
- instructors notes
- datasets

Modules are the glue that brings the rest of the content together. Within each module file, we define a series of slides. Slides may contain text (i.e. bullets), figures, examples, and instructor notes. Exercises are similar in that they too are also composed of slides; however, since exercises are typically only a relatively small set of instructions to students, the bulk of the content in this repository is in modules.

Modules
-------

You may find all modules for MongoDB training in the `<source/modules>`_ subdirectory. The convention for naming modules is to begin with the name of the section in which the module will usually be presented to students, followed by a label for the topic the module addresses. Use hyphens to separate words and ``.txt`` as the filename extension. This convention enables us to easily locate all modules in a section in a directory listing. The `indexes` section provides a good example. The modules in that section are as follows:

- `<source/modules/indexes-fundamentals.txt>`_
- `<source/modules/indexes-compound.txt>`_
- `<source/modules/indexes-multikey.txt>`_
- `<source/modules/indexes-hashed.txt>`_
- `<source/modules/indexes-TTL.txt>`_
- `<source/modules/indexes-geo.txt>`_
- `<source/modules/indexes-text.txt>`_

For each module we define a title and one or more (usually many more) slides. The first slide must contain a list of learning objectives for the module. The following snippet from the indexes-fundamentals.txt module provides an example. Please follow the syntax conventions this example illustrates when writing curriculum. In particular please note how the title and slide headers are delimited. Please also note the syntax for creating bullets and including figures. You will also see several examples of defining instructor notes. *Instructor notes are an important part of the curriculum. They help instructors, most of whom deliver training only infrequently, to prepare and play a very important role in helping new instructors ramp.*

.. code::

    ==================
    Index Fundamentals
    ==================

    Learning Objectives
    -------------------

    Upon completing this module students should understand:

    - The impact of indexing on read performance
    - The impact of indexing on write performance
    - How to choose effective indexes
    - The utility of specific indexes for particular query patterns

    .. only:: instructor

       .. note::

         - Ask how many people in the room are familiar with indexes in a relational database.
         - If the class is already familiar with indexes, just explain that they work the same way in MongoDB.

    .. include:: /includes/student-notes.rst



    Why Indexes?
    ------------

    .. include:: /images/btree-index.rst

    .. include:: /includes/student-notes.rst

    .. only:: instructor

       .. note::

          - Without an index, in order to find all documents matching a query, MongoDB must scan every document in the collection.
          - This is murder for read performance, and often write performance, too.
          - If all your documents do not fit into memory, the system will page data in and out in order to scan the entire collection.
          - An index enables MongoDB to locate exactly which documents match the query and where they are located on disk.
          - MongoDB indexes are based on B-trees.


    Types of Indexes
    ----------------

    - Single-field indexes
    - Compound indexes
    - Multikey indexes
    - Geospatial indexes
    - Text indexes

    .. include:: /includes/student-notes.rst

    .. only:: instructor

       .. note::

          - There are also hashed indexes and TTL indexes.
          - We will discuss those elsewhere.


    Exercise: Using ``explain()``
    -----------------------------

    Let's explore what MongoDB does for the following query by using ``explain()``.

    We are projecting only ``user.name`` so that the results are easy to read.

    .. code-block:: javascript

       db.tweets.find( { "user.followers_count" : 1000 },
                       { "_id" : 0, "user.name": 1 } )

       db.tweets.find( { "user.followers_count" : 1000 } ).explain()

    .. include:: /includes/student-notes.rst

    .. only:: instructor

       .. note::

          - Make sure the students are using the sample database.
          - Review the structure of documents in the tweets collection by doing a find().
          - We'll be looking at the user subdocument for documents in this collection.
