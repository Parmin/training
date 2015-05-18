# MongoDB Diagnostics and Debugging

<img src="img/mongodb-university-logo.png" class="floatright single" style="width: 100px">

## Overview

In this workshop, the instructor will introduce useful tools (both supported and external) and problem-solving approaches for a MongoDB deployment, including a series of real-world scenarios involving hardware, network, and other issues.

## Schedule

## 9AM

### Introduction

* Warm Up and Introductions
* MongoDB Overview
* MongoDB Stores Documents
* Components to MongoDB Diagnostics: the MongoDB Server, Application Settings, Hardware Settings

## 9:15AM

### MongoDB Diagnostics

* Finding bad queries and fixing them
* Indexes and utilizing .explain("executionStats")
* Case Study: bad query with sort
* Shard key considerations
* mongod settings (WT compression, smallfiles, etc.)

## 10:30AM Mid-morning Break

## 10:45 

### Application Diagnostics

* Determining where the bottleneck is (database vs application)
* How schema design can effect application performance
* Case study: bad schema design for a social network
* Read preference
* Write concern
* Connection settings

## 11:30AM 

### Hardware Settings

* MongoDB Production Notes
* Disk Settings

## 12:00PM

### Group Exercise

* Use monitoring tools to diagnose the problems (MMS, mtools, mongostat, and mongotop)
* Determine the correct methods to fix the problems

## 12:30PM Lunch

<style>#resources_table{display:none;}</style>