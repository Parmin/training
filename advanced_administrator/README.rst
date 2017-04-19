===========================================================
Advanced Administration Training - Environment Instructions
===========================================================

Hi there, welcome to Advanced Administration Training Setup and Installation Instructions.
These instructions are to be carried out by our instructors to set up the training environment so
students can run the labs for the Advanced Administration.

Detailed instructions are available at:
  https://docs.google.com/document/d/1vhA6NvlTsPe1rw_fb7N5NrYzJ78odiHWBd5yf9vPd64


Feedback
--------

If, as an instructor, you have any feedback about the courses, please make the effort
to collect the information and give it to us.
Different ways to provide us feedback are listed on the following Wiki page:

  https://wiki.mongodb.com/display/DE/How+to+Submit+Feedback+on+MongoDB+Courses


Requirements
------------

For a correct installation of the setup tools you are required to have installed the following dependencies

- `Virtual Env `_
- `AWS Cli`_
- Have a user created on MongoDB Training Instructor group

-- ADD preflightcheck.sh


Execution Steps:
----------------

#. Activate virtual env:

.. code-block:: bash

  virtualenv venv
  source venv/bin/activate


#. Install dependencies:

.. code-block::

  pip install -r requirements.txt

#. Add AWS ``advanced_training`` profile:


.. _`Virtualenv`: https://virtualenv.pypa.io/en/stable/

.. _`AWS Cli`: https://aws.amazon.com/cli/
