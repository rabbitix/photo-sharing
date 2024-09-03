# foto
service for sending photos


how to build:
```shell
docker build -t foto:0.0.1 .
```

how to deploy manually: [(link)](https://stackoverflow.com/a/26226261)
```shell
docker save foto:0.0.1 | bzip2 | pv | ssh alex@23.95.218.149 docker load
```

how to start:

```shell
docker compose up
```

```shell
docker compose down
```





#### docs
- [this helped in queue](https://johnsturgeon.me/2022/12/10/asyncio-queue)
