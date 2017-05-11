==================
Contributors Guide
==================

Contributions
-------------

Before you start editing the content you should fork the `education training repo`_ to your own personal github account.

For each bug/new feature/improvement there should be an associated `EDU JIRA`_ ticket reporting the intended work. If there is not, please create one reporting the intended action.


With that jira ticket one should create a branch with the following format **initials-jira_ticket_id**:


  EDU-2775 - https://jira.mongodb.org/browse/EDU-2775

  Norberto Leite - nl

.. code-block:: bash

  > git checkout -b nl-EDU-2775

Once you are done with code/content you should submit a pull request.


* If you have `push` permissions on the `education training repo`_ you should push of your branch and then perform a pull request.

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


After you create the pull request, you should move the ticket from "In Progress" to "In Code Review" and notify your team mates asking for a code review.

There isn't a strict number of LGTMs but you should only merge once all the subject matter is complete and at least one team member reviewed your material.


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

As you write new content, please use the directive `literalinclude <http://www.sphinx-doc.org/en/stable/markup/code.html#includes>`_ and the options ``start-after`` and ``end-before``. For example, you might have a section

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

Using Figures
-------------

There is an official page in our `docs <https://docs.mongodb.com/meta/images-guide/>`_
to help on the use of figures:


However, I will go in a little more details, especially for this repository.

You will find figures used in training in both the `<source/figures>`_ and `<source/images>`_ subdirectories.

`<source/figures>`_ is linked to the *docs-assets* repository, using the *training* branch.
It is used for shared images between this repository and the docs repositories.
If you make a modification in this directory, it should be on a private branch that will be merged to the *training* repository.
You will need to ask someone in the *Docs* team to do the review.
Note that committing to this repository may take more cycles, and that it is a **public repository** that the customers can clone, so beware of adding confidential information.

`<source/images>`_ contains local images to this repository, mostly ``.svg`` files.
The ``metadata.yaml`` file define which images we use and at what sizes they should be generated for the different targets (i.e. pdf, HTML, slides).

If you are creating a new image, do it in *SVG* format.
If you are given a ``.png`` or ``.jpg``, you will need to generate the corresponding ``.eps``.
See the following example on how to generate a ``.eps`` file from a ``.png`` on your Mac.
Note that trying to install ``imagemagick`` with ``brew`` may conflict with ``macports``, if you are using the latter.

Aside from generating a ``.eps`` file for your non-SVG images, you will also need to create a ``.rst`` file and provide some metadata.
Look in the ``figures_local_meta`` folder for examples. After creating this ``.rst`` file, you include your image with ``.. include:: /figures_local_meta/corresponding-image.rst``

Alternatively, you can execute the ``build_images.py`` script in the source directory of the images you want to include. Do **NOT** do this in ``source/images``. This script will generate a ``.eps`` and a ``.rst`` file for every ``.jpg`` or ``.png`` file found in the directory you run it in. You will then need to copy all of the files to the appropriate directories.

.. code::

    brew install imagemagick
    convert temp.png eps3:temp.eps

Again, if the file is to be shared by the MongoDB documentation, it should go in the ``docs-assets`` repository (`<source/figures>`_).
If the file is not be shared, you should checked it in `<source/images>`_

Some examples:

- shared/public SVG file

  - ``source/figures/relationship-to-zillions.svg``
  - ``source/images/relationship-to-zillions.svg``   (soft link)
  - metadata goes in ``source/images/metadata.yaml``

    - type: web  will control the size in the html pages
    - type: web  will also control the size in the slides (which are also html!)

  - referenced in ``source/modules/internal/schema-design.txt``

- shared/public non-SVG file

  - ``source/figures/wt-page-reconciliation.eps``
  - ``source/figures/wt-page-reconciliation.png``
  - ``source/figures_meta/wt-page-reconciliation.txt``
  - referenced in ``source/modules/internal/storage-engines-wired-tiger.txt``

- training only SVG file

  - ``source/images/sharding-splitting.svg``
  - metadata goes in ``source/images/metadata.yaml``
  - referenced in ``source/modules/sharding-balancing.txt``

- training only non-SVG file

  - `<source/images/internal-file-format.eps>`_
  - `<source/images/internal-file-format.jpg>`_
  - `<source/figures_local_meta/internal-file-format.txt>`_
  - referenced in `<source/modules/internal/storage-engines-mmapv1.txt>`_

Creating figures
----------------

Here a quick checklist of the steps I used to create the figures for the schema design module.

- create the figure in Google Draw
- download the figure as ``.svg``
- copy the ``.svg`` into ``source/figures``
- link the svg from ``source/images``
- add the image to ``source/images/metadata.yaml``

  - a typical 'output' section would look like::

        output:
           - type: print
             tag: 'print'
             dpi: 300
             width: 1600
           - type: 'web'
             dpi: 72
             width: 450
           - type: 'offset'
             tag: 'offset'
             dpi: 300
             width: 200

  - no worry about adding or not quotes for the values, as it is not needed in YAML
  - the 'web' type is for the HTML and Slides modes
  - the 'offset' type is to generate the EPS image that goes in the PDF
  - the 'print' type is for generating PNG (from svg). We are not sure if this is used

- add a line like the following in the rST files

  - .. include:: /images/pattern-cache.rst

Labs
----

You will find labs in the `<source/exercises>`_ subdirectory. The above discussion on creating slides, including examples, and writing instructors notes applies to labs as well. Labs are simply modules that require active participation from students. Labs should have especially well defined learning objectives. You should be very clear about what students should be able to do after having completed a lab and the lab should fulfill that contract with the student. Labs are learning by doing and students should walk away from a lab being able to apply what they've learned to their own use cases.

Tools and Editors
-----------------

There's a plenitude of different good editors out there for *rST* editing.

Atom Editor
~~~~~~~~~~~

`Atom`_ is a very nice editor that allows a great deal of customization and with a vast number of plugins.

If you want to preview the *rST* files with `Atom`_:

- install the plugin: `restructured text preview Pandoc`_

  which will require that you also install the plugin *language-restructuredtext* and the command line tool *Pandoc*. See the above plugin documentation for more details on how to install those dependencies.

- install Pandoc with: brew install pandoc
- ensure the file that is opened in the editor is recognized as *reStructuredText*. If not, click on the type at the right bottom of the window and select *reStructuredText*.
- Using the keys ``Shift + Control + E`` should open a window to the right of the page and display it in *rST*, minor the pre-processing stuff that should be handled by *Giza*.

If you are a fan of ``vi``, you can still use `Atom`_ to preview your file as you edit it with your favorite editor.
Upon saving in ``vi``, `Atom`_ will automatically refresh the previewed page.

.. _`education training repo`: https://github.com/10gen/training
.. _`EDU JIRA`: https://jira.mongodb.org/browse/EDU
.. _`Atom`: https://atom.io/
.. _`restructured text preview Pandoc`: https://github.com/tohosokawa/rst-preview-pandoc


Restview Viewer
~~~~~~~~~~~~~~~

*Restview* is another tool you can use to render *rST* pages.
Here are the commands to install it and use it

.. code::

  pip install restview
  # opens a web page and serves up the file; changes view as you save.
  restview filename.rst

Building the artifacts
----------------------

Build the slides with

.. code::

    make instructor-package

In order to build the *PDF*, you will need to install *LaTeXiT* and *MacTex*. Then run:

.. code::

    make latex

If you want to build a PDF, you will need to:

- add the description of the PDF to the file `<config/pdfs.yaml>`_
- add a corresponding file in "source/meta", which should point to a section in "source/includes"

More details about the internals
--------------------------------

Architecture of a PDF
~~~~~~~~~~~~~~~~~~~~~

If you create a new PDF, it may be difficult to tell which file or section is creating an error in trying to build the PDF file.
So, here is a quick example on how files are organized.
Often, the issue is coming from the figures/images, so you may want to build your PDF without those to ensure your files are organized correctly, then add the images.
If the issue is with running ``pdflatex``, look for errors in the logs into the directory ``build/<branch>/latex-<target>/*.log``.

Here are the dependencies between the files in the repository in order to build a PDF file. Let's look ``admin-three-day-instructor-guide.pdf`` as an example.

- the PDF is listed in `<config/pdfs.yaml>`_

  It shows the source as ``source: 'meta/admin-three-day'``

- which points to the file `<source/meta/admin-three-day.txt>`_.

  This file contains a list of chapters. Each of the chapter will have a file in the ``source/modules/nav`` directory.

  The list of chapters will appear as the top level tree in the left window and the chapters will be numbered 1, 2, 3, ...

- in our example, the second chapter is described by `<source/modules/nav/crud.txt>`_.

  The file starts with a header **"CRUD"**, which is what is contributed to the table of contents as the chapter name.
  The file contains the following lines:

  .. code::

      .. include:: /includes/toc/dfn-list-crud.rst
      .. include:: /includes/toc/crud.rst

  which are more of an indication to *Giza* about what to build.

  In reality, it points to the file `<source/includes/toc-crud.yaml>`_.

  This is obtained by changing the ``/`` by a ``-`` after ``toc``.

- `<source/includes/toc-crud.yaml>`_ lists the lessons and exercises for the chapter.

  Those will appear as the second level in the document tree and will be numbered 2.1, 2.2, 2.3, ...

  Finally, we point to the *rST* files with the real contents.

  Note that the text reflected at that level in the doc tree will be taken from the headers of the files it points to.

- in our example, the first lesson is `<source/modules/crud-creating-and-deleting-documents>`_

  Similarly to the first names of the chapters, the names of the lessons come from the header of each lesson, and this is what is displayed in the left window of the PDF file. In this case *Creating and Deleting Documents*, instead of what was in the ``toc-crud.yaml`` file.

  In those pages, you will likely have images.
  See the section on adding images for more information.

Architecture of HTML contents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you understood the architecture of PDF files, this section is much easier.
Let's look at the the course corresponding to the PDF file we looked at earlier.

- in our example, the top file is `<source/modules/agenda-dba-3-days.txt>`_.

  This file contains the contents that get rendered as you main HTML page.
  This document mostly reference *lessons* directly, however if you want to see a similar agenda that points to *chapters* instead of *lessons*, you are likely going to point to a sub agenda. For example, look at ``source/modules/internal/agenda-nhtt.txt`` which includes the sub agenda ``source/modules/internal/agenda-nhtt-security.txt``.

- once built, you can open the top level agenda, or any lessons.

  All HTML pages for a giving agenda are available through `<build/instructor-package/modules>`_.

- The left window in the HTML pages is created from `<source/includes/toc-contents.yaml>`_.

  Regardless of the contents of a class, all the available contents can be accessed through this list.
  This file has a references to chapters in the ``nav`` directory that will contain list of lessons back to this ``includes`` directory, and finally pointing to contents in the ``modules`` directory. This is very similar to what we saw earlier in the PDF architecture.

  This main index is very similar to the files we find in ``meta``, however lives in ``includes``.
  There's a reason but it's difficult to explain in text. The TL DR is that it's a vestige of the training repo emerging from docs. We are stuck with it for now. But we would like to remove the layer of indirection that embodies.

Architecture of slide contents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Not much is different from the *HTML* contents.
Those live in a parallel directory to the *HTML* contents, in ``build/instructor-package/slides``.
Each *HTML* content page as a *URL* to the corresponding *slide*.

Beware that the *HTML* and *slides* modes may not render exactly the same way, so you should preview both formats.
