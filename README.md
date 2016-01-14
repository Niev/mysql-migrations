What is it?
---
mysql-migrations is a tool to one by one execution of migrations into your database.
It keeps history of already applied migrations directly in your database and uses `Migrations` table for this purpose.

What is a migration?
---
Migration is a SQL file with one or more MySQL statements. Statements separated with comma ";".

Philosophy of mysql-migrations
---
One folder for database migrations
One migration file for change
No structure rollbacks (they insecure in most cases)
All migrations under CSV with project

Usage
---
It search migrations in `/migrations` folder and do nothing if it is empy.

    docker run -v migrations:/migrations -e MYSQL_ROOT_PASSWORD=<..> -e MYSQL_DATABASE=<..> niev/mysql-migrations
