===========================================================
Advanced Administration Training - Environment Instructions
===========================================================

Hi  there, welcome to Advanced Administration Training Setup and Installation Instructions.
These instructions are to be carried by our instructors to setup and training environment so
students can run the labs for the Advanced Administration.

Requirements
------------

For a correct installation of the setup tools you are required to have installed the following dependencies

- `Virtual Env `_
- `AWS Cli`_
- Have an user created on MongoDB Training Instructor group

-- ADD preflightcheck.sh


Execution Steps:
----------------

#. Activate virtual env:

.. code-block:: bash

  virtualenv venv
  source venv/bin/activate


#. Install dependencies:

.. code-block::

  pip install requirements.txt

#. Add AWS ``advanced_training`` profile:


.. _`Virtualenv`: https://virtualenv.pypa.io/en/stable/

.. _`AWS Cli`: https://aws.amazon.com/cli/
