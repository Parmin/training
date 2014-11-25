================
MongoDB Training
================

Status
------

We are currently field testing the following sections in a number of public and private trainings:

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

Overview
--------

This project is a comprehensive revision of MongoDB training materials
used for the following classes:

-  MongoDB Essentials Training
-  MongoDB Developer Training
-  MongoDB Admin Training

The build environment has many dependencies. We recommend you retrieve materials from the `presentations`_ directory of the repo. See the Test-Driving
Built Materials section below for instructions on using the html instructor materials and slides.

Objectives
----------

-  To support instructors in learning and delivering MongoDB trainings
   by providing the following resources:

   -  A easily-navigated instructor guide complete with outline, training
      content, and instructor notes

   -  Figures, slides, exercises, and notes for delivery in class

   -  A workbook to be distributed to students to enable them to easily
      follow lessons and exercises and take notes

-  Training materials that are easier to maintain and that encourage
   contributions in the form of pull requests from those who deliver
   MongoDB training and others in the company

-  Modular materials for greater flexibility in how trainings are
   organized

Test-Driving Built Materials
----------------------------

Do a pull on the repo and unzip presentations/instructor-package.tar.gz. This package contains the instructor guide and presentation slides.

Open the contents.html file in a web browser.

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

.. _presentation : https://github.com/mongodb/docs-training/blob/master/presentation
