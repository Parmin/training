# MongoDB Advanced Operations Training

<img src="img/mongodb-university-logo.png" class="floatright single" style="width: 100px">

## Overview


### Introduction

Advanced Operations Training is designed for operations staff responsible for maintaining MongoDB applications. The instructor leads teams through a series of scenarios that represent potential issues encountered during the normal operation of MongoDB. Teams are hands-on throughout the course, actively working together to identify and implement solutions. The instructor evaluates teams based on the speed, elegance, and effectiveness of their solutions and provides feedback on strategy and best practices.

Each scenario develops skills in critical areas such as diagnostics, troubleshooting, maintenance, performance tuning, and disaster recovery. Teams will work in Amazon EC2 instances prepared for this training. The instructor will distribute connection details when the training begins. The scenarios for this training fall into four subject areas as follows.


## Day 1


### Backup and Recovery

If you use a backup service like MMS Backup, then most of the time you don’t have to worry about backup. But when something breaks your production data, manual care may be required to repair it. In this section, students work through an extended exercise restoring a single collection to a previous point in time.


### Replication

Most production deployments of MongoDB should use replica sets, which provide automatic failover. In this section you’ll learn to do the following with minimal downtime:

* Roll out upgrades (with a single failover)
* Roll out performance fixes (with a single failover)
* Diagnose and fix a downed node (with no downtime)


### MMS Automation

MongoDB Management Service (MMS) Automation enables users to auto-provision and deploy MongoDB in standalone nodes, replica sets, and sharded clusters. Automation functionality includes database creation, modification, upgrades, and downgrades.
In this section, students work through an exercise upgrading a MongoDB cluster using MMS Automation.


## Day 2

### The MongoDB Profiler

The scenarios in this section will provide students with experience using the MongoDB profiler. Students will also gain familiarity with the MongoDB aggregation framework as a tool for analytics. Specific scenarios include:

* Using profiling data to find slow operations
* Writing aggregation queries for reporting and diagnostics


### Sharding and Performance Troubleshooting

In this section students learn to diagnose and fix a wide variety of issues that may arise in a sharded cluster:

* Rogue queries (a single query that monopolizes the system)
* Poorly optimized queries (application queries that can be improved)
* Missing indexes
* Bad operating system settings


<style>#resources_table{display:none;}</style>