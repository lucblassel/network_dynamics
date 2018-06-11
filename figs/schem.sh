#!/bin/bash

# script to reverse engineer database schema from database file

#Path to schemaCrawler executable
SchemaCrawlerPATH=/home/zlanderous/Downloads/schemacrawler-14.20.03-distribution
# The path of the SQLite database
SQLiteDatabaseFILE=databaseRomain.db
# The type of the database system.
RDBMS=sqlite
# Where to store the image
OutputPATH=schemRomain.png
# Username and password need to be empty for SQLite
USER=
PASSWORD=

java -classpath $(echo ${SchemaCrawlerPATH}/_schemacrawler/lib/*.jar | tr ' ' ':') schemacrawler.Main -server=${RDBMS} -database=${SQLiteDatabaseFILE} -outputformat=png -outputfile=${OutputPATH} -command=details -infolevel=maximum -user=${USER} -password=${PASSWORD}
