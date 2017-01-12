==============================
Schema Design Instructor Notes
==============================

I did schema design in a two-phase lesson.

Phase I
-------

I talked about the basic principles of schema design, and how they're in conflict:

* Embed and denormalize to minimize number of queries

  * More efficient reads, less efficient writes

* Normalize and reference to minimize extraneous data getting pulled into the cache
* Showed them some slides from "basic principles"
* I gave them a basic books/authors/reviewers schema, like the one in the 'basic principles' slide
* I told them there's some great advice on Zola's blog posts:

  * http://blog.mongodb.org/post/87200945828/6-rules-of-thumb-for-mongodb-schema-design-part-1
  * http://blog.mongodb.org/post/87892923503/6-rules-of-thumb-for-mongodb-schema-design-part-2
  * http://blog.mongodb.org/post/88473035333/6-rules-of-thumb-for-mongodb-schema-design-part-3

Results of Phase I
------------------

* A lot of bad schemas.

  * Arrays growing without bound
  * Not much discussion of indexes
  * No queries written


Lessons after Phase I
---------------------

* Asked how many of them could name 2 of Zola's 6 principles; nobody could.
* Showed them the blog, part 3.
* Talked about the mistakes they were making.
* Walked them through the principles
* Gave them the old "online marketplace" application problem that I got while onboarding.

  * 1.5 hours to do it
  * I would want:

    * Documents
    * Queries
    * Indexes

* After 20 minutes, walked around and asked to see queries. Nobody had any, so I told them to build them based on whatever functionality they had already decided upon.


