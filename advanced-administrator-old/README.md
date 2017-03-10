Wargaming Summary
-----------------

Wargaming is a 1 day consulting engagement at the customer site. It consists of
splitting the students into teams and running a set of scenarios on MongoDB
that pits each team against each other in a bid to identify and provide a
solution to the problem put in front of them. Teams are awarded points on
speed, elegance, and effectiveness of their solution. The winning team receives
a prize.

Wargaming is an entirely practical set of exercises, where teams are hands on
throughout the day, actively working together to identify and implement a
solution.

This session is designed for 4-12 people.

Instructor and Student Guides
-----------------------------

First get a local copy of the repo and change into the Training/wargaming
directory on your local machine:

``cd wargaming``

Then you can build the instructor guide and the student guide by issuing:

``make all``

If the command ``rst2pdf`` is not found and you're on a Mac, install homebrew
(http://brew.sh/) and then run the following commands:

``brew install libjpeg``

``sudo easy_install --upgrade pip``

``sudo easy_install --upgrade PIL``

``sudo pip install --upgrade rst2pdf``

If the command ``pdflatex`` is not found and you're on a Mac, grab the
installer from http://tug.org/mactex/ (it's 2.3 GB!).

The guides for both the instructors and the students will be built and stored
in the ``build`` directory as PDF's.

If you need to make any changes to the text in either guide, the text is stored
in ``src/sections`` which is what is pulled together by the make file to make
the PDF's.


Sales Qualification
-------------------

For wargaming to be successful, it must have:

- 4 to 12 people.
- A training room with projector and white board.
- One machine per team of people (3-4 people per team).
- Outside Internet access, both HTTP and SSH
- Linux operating systems. If Windows is required, please get in touch, (see
below), as we may be able to make this happen for certain customers.

If any of these criteria fail then this is a NO SELL right now. If you have a
partial criteria, or are unsure of anything, please email
sam.weaver@mongodb.com for clarification.
