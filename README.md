# Database Project for DBMS-3:
### Tech

Build on top a web micro-framwork `Flask`

- [flask] - [web development, one drop at a time](https://flask.palletsprojects.com/en/2.0.x/)
- [MariaDB] - [mysql installation](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/)
- [Python3] - [python3](https://www.python.org/downloads/)
- [Environment] - [Python with pip+venv](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

### Run (Bash)

*-> Pre-requisites*

```sh
python3 -m venv venv
```
```sh
source venv/bin/activate
```
```sh
pip install -r requirements.txt
```
*-> Running webserver in development mode (with hot loading)*

```sh
export FLASK_ENV=development
```

To run on a desired port:

```sh
export FLASK_RUN_PORT=your_desired_port
```
*-> Here we go...*

```sh
flask run
```
