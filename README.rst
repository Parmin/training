================
MongoDB Training
================

Overview
--------

This repository contains the MongoDB training materials used for the following classes:

-  MongoDB Essentials Training
-  MongoDB Developer Training
-  MongoDB Admin Training

Instructor and student are in the `presentation`_ directory of the repo. See the `Using Instructor Materials`_ section below.

Objectives
----------

-  To support instructors in learning and delivering MongoDB trainings
   by providing the following resources:

   -  A easily-navigated instructor guide complete with outline, training
      content, and instructor notes

   -  Figures, slides, exercises, and notes for delivery in class

   -  A workbook to be distributed to students to enable them to easily
      follow lessons and exercises and take notes

-  Training materials that are easy to maintain and that encourage
   contributions in the form of pull requests from those who deliver
   MongoDB training and others in the company

-  Modular materials for greater flexibility in how trainings are
   organized

Using Instructor Materials
--------------------------

Do a pull on the repo, unzip `presentation/instructor-package.tar.gz`_, and open **contents.html**.

.. figure:: https://s3.amazonaws.com/edu-static.mongodb.com/training/images/contents.png
   :alt: Contents page

The nav on the left enables instructors to browse the modules in the
instructor guide. Each subsection is designed to be one slide’s worth of
material.

.. figure:: https://s3.amazonaws.com/edu-static.mongodb.com/training/images/instructor_guide.png
   :alt: Contents page

For presentation to students, we have deployed a version of these
materials in the form of slides. To see the deck for a given module,
navigate to that module in the instructor guide and click the slides
link at the bottom of the navigation pane.

.. figure:: https://s3.amazonaws.com/edu-static.mongodb.com/training/images/instructor_guide_click_slides.png
   :alt: Contents page

This will bring up another browser window containing html-based slides.
These decks respond to keyboard events such as arrow keys and the space
bar in the same way as Microsoft Powerpoint.

Status
------

Completed sections include:

-  Introduction
-  CRUD
-  Indexes
-  Aggregation
-  Data Modeling
-  Replica Sets
-  Sharding
-  Security
-  Performance Troubleshooting
-  Backup and Recovery

We need to include a section on MMS.


.. _presentation : https://github.com/mongodb/docs-training/blob/master/presentation

.. _presentation/instructor-package.tar.gz : https://github.com/mongodb/docs-training/blob/master/presentation/instructor-package.tar.gz
