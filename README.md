# Teammaker

Teammaker is a simple App to create balanced teams.
python modules used:
- wxPython for Graphics
- django for database and ORM

## How to Install

If you use a virtualenv install requirements via pip:

```
pip install -r requirements.txt
```

Now Create database
```
> python manage.py makemigrations teammaker
Migrations for 'teammaker':
  teammaker\migrations\0001_initial.py:
    - Create model Player
    ...
```

and:

```
> python manage.py migrate
Operations to perform:
  Apply all migrations: teammaker
Running migrations:
  Applying teammaker.0001_initial... OK
```

when database players.db is created, run application:

```
>python main.py
```


### Create and Edit players

From menu Players, select submenu 'New player' to save a new player to database.
Fill field surname, name, value (player skills), health and role.
To change player values select submenu 'Edit Player'.
A summary of all database players is available from submenu 'Player summary'.
it is possible to edit player directly from player summary.


### Crete teams

Select players from main frame and click generate.
If GAP is correct, the app will create balanced teams with 5000 attempts,
otherwise you have to increase GAP from 'menu GAP'.
When teams are balanced they will appear in the right listboxes.
If number of players is odd, the app will add automatically a NULL player but
to create teams succesfully you must to set GAP higher.

## License

GPL
