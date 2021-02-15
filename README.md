# DanDanPlaySearchService

根据 [弹弹play资源搜索节点API规范](https://github.com/kaedei/dandanplay-libraryindex/blob/master/api/ResourceService.md) 开发的服务端API，支持docker。

## 直接运行

```bash
git clone https://github.com/Lava-Swimmer/DanDanPlaySearchService.git
cd DanDanPlaySearchService
chmod +x ./install.sh
chmod +x ./start_local.sh
./install.sh
./start_local.sh
```

## 使用docker

### docker-cli

```bash
docker pull lavaswimmer/dandanplaysearchservice:latest
docker run -d -p 9145:9145 --name ddpss lavaswimmer/dandanplaysearchservice
```

### 或者docker-compose

新建文件`docker-compose.yml`

```yaml
version: '3.3'
services:
    ddpss:
        container_name: ddpss
        image: 'lavaswimmer/dandanplaysearchservice:latest'
        ports:
            - '9145:9145'
        restart: unless-stopped
```

然后执行`docker-compose up -d`
