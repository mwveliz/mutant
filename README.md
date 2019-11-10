# Project Title

Mutants for ML

## Getting Started

This projects asks if DNA is mutant or ont based on 4 in line rules,
it also insert into a self contained sqlite database  and then gives basic
statistics and rate of mutants vs humans,.

### Prerequisites

python3 and pip
.env file with addres of the server and sqlite3 database name
for example: (.env file)

```
SERVER=localhost
DATABASE=mutant.db
```

### Installing

Use pip to install all the dependencies

```
pip3 install -r requirements.txt 
```


End with an example of getting some data out of the system or using it for a little demo

## Running the tests and coverage

For running the tests use pytest this will put the server up and test


```
pytest test.py
```

See coverage on coverage report

```
coverage.py report
```

### Swagger

You can understand better the endpoints visiting swagger

```
18.204.21.240:5000/apidocs
```

## Deployment
For production a demonized it using pm2, but for deployong locally you can just
run app.py using python
```
python3 app.py
```

## Built With

* Python3
* Sqlite3
* Flask

## Versioning

This is version 2.0.0 because the previous attemp was servrles and wan not so 
good to understand
## Authors

* **Miguel Delgado Veliz

## License

This project is licensed under the GPL-V3 License 

## Acknowledgments

* To me

