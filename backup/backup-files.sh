#!/bin/bash
tar -czvf files/gea_$(date +%F).tgz ../../gea/* --exclude=gea*.*gz

