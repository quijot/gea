#!/bin/bash

psql -d gea -f triggers.sql
psql -d gea -f data.sql
