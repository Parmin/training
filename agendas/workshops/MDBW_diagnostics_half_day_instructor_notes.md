# MongoDB Diagnostics and Debugging

<img src="img/mongodb-university-logo.png" class="floatright single" style="width: 100px">

## Overview

In this workshop, the instructor will introduce useful tools (both supported and external) and problem-solving approaches for a MongoDB deployment, including a series of real-world scenarios involving hardware, network, and other issues.

## Schedule

## 9AM

### Introduction

* Warm Up and Introductions
	- Ask the students their backgrounds and knowledge of MongoDB (e.g. have you had any performance issues, how did you fix them?)
* MongoDB Overview 
	 - In case any students don't have an understanding of how MongoDB work (documents, collections, etc.)
* MongoDB Stores Documents
* Components to MongoDB Diagnostics: the MongoDB Server (indexes, operations), Application Settings (schema, driver settings), Hardware Settings (disk settings, ulimits, etc.)
	- These are the three main components this course with focus on

## 9:15AM

### MongoDB Diagnostics

* Finding bad queries and fixing them
	- Badly indexed queries account for the vast majority of performance issues, this section is the largest
	- Work through the index section of our in-person training materials
* Indexes and utilizing .explain("executionStats")
	- Work through the index section of our in-person training materials
	- Explain how to optimize a query with .explain("executionStats"), make sure to cover sorting
	- Explain for write operations (remove, update, etc.), how it works
* In-class exercise:

::

	for (var i=0; i<1000; i++) { db.blog.insert( { "headline" : i, "date" : i + 1, "section" : i+2 } ); }

	- db.blog.find( { "headline" : 200 } )
	- db.blog.find( { "headline" : 200, section: 50 } ) - which order should the index be in?
	- db.blog.find( { "headline" : 200 }).sort( { "date" : -1 }) - index?

* Case Study: bad query with sort
	
You've created a blog comment system, it contains four comments (insert each to the database in front of the class)::

	db.comment.insert({ timestamp: 1, anonymous: false, rating: 3 })
	db.comment.insert({ timestamp: 2, anonymous: false, rating: 5 })
	db.comment.insert({ timestamp: 3, anonymous:  true, rating: 1 })
	db.comment.insert({ timestamp: 4, anonymous: false, rating: 2 })

Create an index to optimize the following query::

	db.comment.find({ timestamp: { $gte: 2, $lte: 4 }, anonymous: false })

Add index {timestamp:1, anonymous:1} vs {anonymous:1, timestamp:1} ?

Now optimize the query::
	
	db.comment.find({ timestamp: { $gte: 2, $lte: 4 }, anonymous: false }).sort( { rating: -1 } )

What are the index choices? Experiment with each.

After working through all the possibilities, the following index is the best for this (very contrived) example (this index isn't very intuitive to many users)::
	
	db.comments.ensureIndex({anonymous:1, rating:1, timestamp:1});

* mongod settings (WT compression, smallfiles, etc.)

	- Compression algorithms with WT: Zlib, Snappy, none
	- Smallfiles effects file size allocation performance (relevant to MMAP)

* Killing bad queries (db.currentOp())

## 10:30AM Mid-morning Break

## 10:45 

### Application Diagnostics

* Determining where the bottleneck is (database vs application)
	- How long does it take to deserialize an object from the database?
	- How long does it take to establish a connection to the database, or we efficiently pooling connections?
* How schema design can effect application performance
	- Walk through the different ways to design a CMS, denormalize the author information for articles will have what impact? Etc.
* Shard key considerations
	- Design a Google analytics competitior, tradeoffs for shard keys: (siteid (for for writes) vs hashed[_id] (good for writes, bad for reads)
* Case study: bad schema design for a social network
	- The Socialite feed service is a good case study (schema design here will greatly effect application performance): https://github.com/10gen-labs/socialite/blob/master/docs/feed.md
* Read preference
* Write concern
* Connection settings

## 11:30AM 

### Hardware Settings

* MongoDB Production Notes
	- NUMA, ulimits, readahead for MMAP, TCP Keepalive (not in production notes)
	- MongoDB production notes: http://docs.mongodb.org/manual/administration/production-notes/
* Disk Settings
	- RAID 10 vs RAID 0 with MongoDB replication
	- SSD vs spinning disks
* TCP Keepalive?

## 12:00PM

### Group Exercise

* Use monitoring tools to diagnose the problems (MMS, mtools, mongostat, and mongotop)
* Determine the correct methods to fix the problems
	- Hostnames to use for exercises coming soon

## 12:30PM Lunch

<style>#resources_table{display:none;}</style>