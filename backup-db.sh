#!/usr/bin/env bash
# Usage: ./backup-db.sh <backup-dir>/
GEA_DB_DIR=${1}'backup/db/gea-db_'$(date +\%w)
rm -r $GEA_DB_DIR
echo "Backing DB up to $GEA_DB_DIR."
pg_dump -Fd gea -f $GEA_DB_DIR -Z 9 --data-only --no-owner --column-inserts -T 'auth_*' -T 'django*'
pg_dump -d gea -f $GEA_DB_DIR/gea-schema.sql.gz -Z 9 --schema-only --no-owner --column-inserts -T 'auth_*' -T 'django*'
echo "Done."
