#!/bin/bash

cd "$(dirname "$0")"
psql -d gea -f triggers.sql
psql -d gea -f data.sql
