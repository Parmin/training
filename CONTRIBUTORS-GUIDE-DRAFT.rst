==================
Contributers Guide
==================

Contributions
-------------

Before start editing the content you should fork the `education training repo`_ to your own personal github account.

For each bug/new feature/improvement there should be an associated `EDU JIRA`_ ticket reporting the intended work. If there is non please create one reporting the intented action.

With that jira ticket one should create a branch with the following format **initials_jira-ticket-id**:

  EDU-2775 - https://jira.mongodb.org/browse/EDU-2775

  Norberto Leite - nl

.. code-block:: bash

  > git checkout -b nl-EDU-2775

Once you done with code/content you should submit a pull request.

* If you have `push` permits on the `education training repo`_ you should push of your branch and then peform a pull request.

.. code-block:: bash

  > git remote -v
  origin	git@github.com:10gen/training.git (fetch)
  origin	git@github.com:10gen/training.git (push)
  > git push origin nl-EDU-2775

* If you don't then you need to push your branch to your forked version of the `education training repo`_ and then perform a pull request

.. code-block:: bash

  > git remote -v                                                                                                                                                                                                 [10:39:19]
  nleite	git@github.com:nleite/docs-training.git (fetch)
  nleite	git@github.com:nleite/docs-training.git (push)
  > git push origin nl-EDU-2775

After you created the pull request you should move the ticket from in-progress to Code Review and notify your team mates asking for a Code Review.

There isn't a strict number of LGTM's but you should only merge once all the subject matters and at least one team member reviewed your material.


Source
------

The source for the curriculum in this repository is found in the `source`_ subdirectory. We model curriculum as follows:

- modules (e.g., compound indexes)
- examples
- instructors notes
- labs
- figures or images
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

For each module we define a title and one or more (usually many more) slides. The first slide must contain a list of learning objectives for the module. Please write active learning objectives. You should describe what students will be able to do upon completing the module. The following snippet from the indexes-fundamentals.txt module provides an example. Please follow the syntax conventions this example illustrates when writing curriculum. In particular please note how the title and slide headers are delimited. Please also note the syntax for creating bullets and including figures. You will also see several examples of defining instructor notes.

.. code::

    ==================
    Index Fundamentals
    ==================

    Learning Objectives
    -------------------

    Upon completing this module students should be able to:

    - Describe the impact of indexing on read performance
    - Describe the impact of indexing on write performance
    - Define effective single-key indexes for simple data-access patterns
    - Assess the utility of a given index for specific query patterns

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
          - We will be looking at the user subdocument for documents in this collection.


Instructor Notes
----------------

Instructor notes are an important part of the curriculum. They help instructors, most of whom deliver training only infrequently, to prepare and play a very important role in helping new instructors ramp. Instructor notes are visible only to instructors and available in the instructor versions of the training manuals, the html version of the curriculum, and in the slides through the presenter console. Please write instructor notes that will enable consulting engineers and others who deliver training ramp, prep, and deliver training more effectively.


Examples
--------

In most cases, examples illustrating code and data are embedded in the content for a module. We did this originally to make examples easier to code review. In the near future we will be moving all examples into standalone files so that they can be more easily tested.

As you write new content, please use the directive `literalinclude <http://www.sphinx-doc.org/en/stable/markup/code.html#includes`_ and the options ``start-after`` and ``end-before``. For example, you might have a

.. code::

    Sample Dataset
    --------------

    Mongoimport the ``companies.json`` file:

    .. literalinclude:: /includes/aggregation_scripts.sh
        :language: bash
        :start-after: # import companies.json
        :end-before: # end import companies.json

    - You now have a dataset of companies on your server.
    - We will use these for our examples.

In the included file you would then have a section something like the following.

.. code::

    #!/usr/bin/env bash
    # Contains bash scripts for aggregation

    # import companies.json
    mongoimport -d training -c companies --drop companies.json
    # end import companies.json

Figures
-------

You will find figures used in training in both the `<source/figures>`_ and `<source/images>`_ subdirectories. `<source/images>`_ contains a subset of the ``.svg`` images maintained by the documentation team for the MongoDB manual and other docs. the ``metadata.yaml`` file define which images we use for training and at what sizes they should be generated for the different targets (i.e. pdf, HTML, slides). We also contribute ``.svg`` files to this repository that we need to create for training. `<source/figures>`_ contains ``.png`` files and other images that we use (in a pinch) in training. There are not many of these files and, in general, if you are going to create a figure, you should create an ``.svg`` and place it in `<source/images>`_.


Labs
----

You will find labs in the `<source/exercises>`_ subdirectory. The above discussion on creating slides, including examples, and writing instructors notes applies to labs as well. Labs are simply modules that require active participation from students. Labs should have especially well defined learning objectives. You should be very clear about what students should be able to do after having completed a lab and the lab should fulfill that contract with the student. Labs are learning by doing and students should walk away from a lab being able to apply what they've learned to their own use cases.

Editors
-------

There's a plenitude of different good editors out there for rST editing.

* `Atom`_

Atom is a very nice editor that allows a great deal of customization along side with a vast ammount of plugins.
One of the recommended plugings is `restructured text preview Pandoc`_ which gives us a quick preview of our edits.


.. _`education training repo`: https://github.com/10gen/training
.. _`EDU JIRA`: https://jira.mongodb.org/browse/EDU
.. _`Atom`: https://atom.io/
.. _`restructured text preview Pandoc`: https://github.com/tohosokawa/rst-preview-pandoc
