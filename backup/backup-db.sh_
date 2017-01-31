#!/bin/bash
pg_dump gea > db/gea-dump_$(date +%F).sql
gzip --best db/gea-dump_$(date +%F).sql
# para restaurar la db
# $ gunzip gea-dump_yyyy-mm-dd.sql.gz
# $ psql gea < gea-dump_yyyy-mm-dd.sql
