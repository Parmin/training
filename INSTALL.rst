================================
Build MongoDB Training Resources
================================

The training resources use the same tool chain as the MongoDB
documentation.

Install Required Software
-------------------------

In order to generate the figures in the documentation you *must* have
a copy of Inkscape. If you're using a Linux system, install Inkscape
from your system's package manager, using one of the following
commands: ::

  sudo apt-get install inkscape
  sudo yum install inkscape
  sudo pacman -S inkscape

For OS X users, install Inkscape using the instructions provided for
`Installing Inkscape <http://www.inkscape.org/en/download/mac-os/>`_
from the Inkscape project. Do not use Homebrew to install Inkscape.

For Windows users, install Cygwin, and ensure the following packages
are selected for installation: ::

    git
    inkscape
    python
    python-setuptools
    texlive
    texlive-collection-latex

(Perform all Windows builds in a Cygwin terminal)

If you do not have pip installed for python, run: ::

    easy_install pip

All other dependencies are Python packages that are dependencies of
`giza <https://pypi.python.org/pypi/giza>`_. You'll also need the `aws-cli
<https://github.com/aws/aws-cli>`_. Install these packages in a *virtual env*
(preferred), or system wide using ``pip``: ::

  pip install giza
  pip install awscli

Configuring AWS
---------------

We use S3 on AWS to store different files that need to be downloaded by
students or instructors. Because of this you'll need to configure the ``aws``
command line tool with your AWS credentials. You can ask `curriculum@10gen.com
<mailto:curriculum@10gen.com>`_ to add you to the **training-aws** account and
issue you your AWS Key ID and Secret Key.

After you have your access key id and secret you can run the following command to
update your ``~/.aws/config`` and ``~/.aws/credentials``.

.. code-block:: bash

  $ aws configure
  AWS Access Key ID: <AWS ACCESS KEY ID>
  AWS Secret Access Key: <AWS SECRET ACCESS KEY>
  Default region name [us-west-2]: us-west-2
  Default output format [None]: json

Updating VMs
------------

Part of our build process with ``make`` diffs tarballs of Vagrant virtual
machines on S3 against what's locally avaliable inside the ``vms`` directory.
If your build is failing because of this, then there are two things you can do
to resolve the build failure:

1. Someone has updated the ``mongodb-training/vms`` S3 bucket and now your
   local repo is out of sync.

   **Solution:** Rebase your branch with master to get the new changes.

2. You've update the ``vms`` directory and the ``mongodb-tranining/vms`` S3
   bucket is now out of sync with your local repo.

   **Solution:** Copy the tarball out of ``build/vms`` and replace it with the
   old tarball on the ``mongodb-training/vms`` S3 bucket. Make sure to make the
   tarball public on S3 so anyone can download it.

Build Resources
---------------

Giza orchestrates all builds; however, there's a ``Makefile``
interface for most interaction that you may find more
approachable. For most day to day work, use the following operation:
::

  make html

This will generate output in the ``build/<branch>/html-student`` and
``build/<branch>/html-instructor`` directories. Substitute
``<branch>``, with your current working branch. You can limit the
build to either the student or the instructor edition, with one of the
following targets: ::

  make html-student
  make html-instructor

To generate slides, you can use the following target: ::

  make slides

Slide output appears in ``build/<branch>/slides-student`` and
``build/<branch>/slides-instructor``. To generate slides *and* html
output in the same operation use the
following target: ::

  make slides-html

To generate the tarball for distribution to instructors, use the
following target: ::

  make instructor-package

Find the compiled package at ``build/instructor-package.tar.gz``.
