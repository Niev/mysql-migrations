This tool apply one by one changes from SQL files in `/migrations` to linked MySQL container.
It keeps history of already applied migrations directly in your database and uses `Migrations` table for this purpose.


What it do?
---
1. Creates database `MYSQL_DATABASE` if not exists
2. Creates table `Migrations` if not exists to keep migrations history
3. Run migrations one by one


Usage
---
    docker run -v path-to-your-migrations:/migrations --link your-mysql-database-container:mysql -e MYSQL_DATABASE=you-mysql-database-name niev/mysql-migrations

`or`

    docker run --volumes-from=container-with-migrations --link your-mysql-database-container:mysql -e MYSQL_DATABASE=you-mysql-database-name niev/mysql-migrations


Environment
---
* MYSQL_DATABASE (`mandatory`)
* MYSQL_USER     (optional, default=root)
* MYSQL_PORT     (optional, default=3306)
* MYSQL_PASSWORD (optional, default=None)
