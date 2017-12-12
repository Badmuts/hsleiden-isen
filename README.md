# hsleiden-isen

## Docker

Currently no volumes are used so nothing is persisted.

```sh
$ docker-compose up -d
```

**Create database**
Not sure if necessary but if there is no db try this

```sh
$ docker-compose exec db /init-influxdb.sh
```

**Install ttn node-red plugin**
For now try this command

```sh
$ docker-compose exec node-red npm install node-red-contrib-ttn && docker-compose restart node-red
```

**Configure Grafana**

* Navigate to `http://localhost:4000`
* Login with `admin:admin`
* Add datasource influxdb
* Use `http://db:8086` as address
* Username: `isen`
* Password `Welkom#1`
* Database: `ttndb`
* Username, password, db can be changed via `docker-compose.yml`

**Configure node-red**

https://www.thethingsnetwork.org/docs/applications/nodered/quick-start.html#configure
