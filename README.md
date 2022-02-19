# dataspaces
Ephemeral Databases for Development

## The pitch

All too often we want to run code against a dev database, when we aren't sure it will work.

But dev databases are often full-scale replicas of production databases, making restoring from backups expensive. 

Also in the modern world our dev databases are cloud based; meaning proxies, VPNs, and so on need setting up. 

It shouldn't be this way.

## The idea

Thankfully, Docker exists, and has lots of tools for this very purpose.

This utility allows you to create a local database for development; snapshot it; run migrations against it; pause it; and roll it back. 

Think of it as Python virtual environments with a docker spin. 

## Ok great, where do I start?

Install the repo

$ dspace setup

$ dspace create --flavour postgres --expose-port 5432 --initial-database my-db --name my-db

$ dspace snapshot mydb snapshot-1 --comment 'before migrations'

$ dspace migrate mydb --tool liquibase --folder migrations/*

$ dspace mydb rollback --to snapshot-1

$ dspace copy mydb newdb 
