# LogAnalysis

LogAnalysis is an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like.

### Tech

LogAnalysis uses a number of tools to work properly:

* [Python](https://www.python.org/) - an interpreted, high-level, general-purpose programming language.
* [PostgreSql](https://www.postgresql.org/) -  free and open-source relational database management system (RDBMS)
* [Oracle VirtualBox](https://www.virtualbox.org/) -free and open-source hosted hypervisor for x86 virtualization.

LogAnalysis requires [Vagrant](https://www.vagrantup.com/) to run the virtual machine and [Git Bash](https://git-scm.com/downloads) to execute commands.


### Design description
LogAnalysis reporting tool consists of three parts represent three Sql queries which execute Sequentially and every query answers a question. Every part is coded as following:

* define Database connection variable.
* define Database cursor.
* using the cursor to execute the query.
* fetching the query result.
* define a (for) loop to print out the result.
* close the database connection.

### Before we start
> All data is stored in PostgreSql database called (news). Before running the tool we must create two Views (most_articles ,  bad_req_days) to let our reporting tool runs.

from [Git Bash] enter vagrant file directory:

1- run the virtual machine:
```sh
$ vagrant up
$ vagrant ssh
```

2- enter the database:
```sh
$ psql -d news                           
```

3- create the views:
```sh
news=>create view most_articles as
select substr(path,10) article,count(path) as num from log where status = '200 OK' group by path order by num desc offset 1;

news=>create view bad_req_days as
select count(status) bad_req_sum , TO_CHAR(time,'Month DD,YYYY') as day from log where status ='404 NOT FOUND'
group by TO_CHAR(time,'Month DD,YYYY') order by count(status) desc;
```

4-exit from PostgreSql:
```sh
news=>Ctrl+d
```

### Run
> /LogAnalysis: contains reporting tool (LogAnalysis.py) 
```sh
$ cd /vagrant/LogAnalysis
$ python LogAnalysis.py
```

