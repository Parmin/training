#!/usr/bin/env bash

# Contains bash scripts for aggregation

# self explanatory
mongoimport -d training -c companies --drop companies.json

