#!/usr/bin/env python3
import os
from mysql import connector
from datetime import datetime

MIGRATIONS_PATH = "/migrations"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

create_db_query = "CREATE DATABASE IF NOT EXISTS `%s` CHARACTER SET utf8 COLLATE utf8_general_ci"
create_table_query = """CREATE TABLE IF NOT EXISTS `Migrations`(
                          `Name` varchar(255) NOT NULL,
                          `Created` datetime NOT NULL,
                          PRIMARY KEY (`Name`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8"""

count_query = "SELECT count(*) FROM Migrations WHERE name = %s"
insert_query = "INSERT INTO Migrations(Name, Created) VALUES (%s, %s)"


if __name__ == "__main__":
    assert os.environ.get("MYSQL_DATABASE")

    migrations = sorted(os.listdir(MIGRATIONS_PATH))
    if len(migrations):
        cnx = connector.connect(
            host="mysql",
            user=os.environ.get("MYSQL_USER", "root"),
            port=os.environ.get("MYSQL_PORT", "3306"),
            password=os.environ.get("MYSQL_PASSWORD"),
            autocommit=True,
        )
        cursor = cnx.cursor()
        cursor.execute(create_db_query % os.environ.get("MYSQL_DATABASE"))
        cnx.database = os.environ.get("MYSQL_DATABASE")
        cursor.execute(create_table_query)
        for file in migrations:
            cursor.execute(count_query, (file,))
            count = cursor.fetchone()
            if count[0]:
                print("{color1}IGNORE{end}: {color2}{migration}{end}".format(
                    color1=bcolors.OKBLUE,
                    color2=bcolors.WARNING,
                    end=bcolors.ENDC,
                    migration=file
                ))
            else:
                print("{color1} APPLY{end}: {color2}{migration}{end}".format(
                    color1=bcolors.OKGREEN,
                    color2=bcolors.WARNING + bcolors.BOLD,
                    end=bcolors.ENDC,
                    migration=file
                ))

                with open(os.path.join(MIGRATIONS_PATH, file)) as migration:
                    list(cursor.execute(migration.read(), multi=True))

                cursor.execute(insert_query, (file, datetime.now()))
        cursor.close()
        cnx.close()
    else:
        print("{color1}There are no migrations".format(
            color1=bcolors.WARNING,
            end=bcolors.ENDC,
            path=MIGRATIONS_PATH
        ))

