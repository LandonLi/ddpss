# DanDanPlaySearchService

根据 [弹弹play资源搜索节点API规范](https://github.com/kaedei/dandanplay-libraryindex/blob/master/api/ResourceService.md) 开发的服务端API，支持docker。

## 本地运行

```bash
git clone https://github.com/Lava-Swimmer/DanDanPlaySearchService.git
cd DanDanPlaySearchService
chmod +x ./install.sh
chmod +x ./start_local.sh
./install.sh
./start_local.sh
```

## docker运行

```bash
docker pull lavaswimmer/dandanplaysearchservice:latest
docker run -d -p 9145:9145 --name ddpss lavaswimmer/dandanplaysearchservice
```