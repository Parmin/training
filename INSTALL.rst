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
`giza <https://pypi.python.org/pypi/giza>`_. Install this package in a
*virtual env* (preferred), or system wide using ``pip``: ::

  pip install giza

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
