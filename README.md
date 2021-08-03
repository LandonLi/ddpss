![GitHub Workflow Status](https://img.shields.io/github/workflow/status/landonli/dandanplaysearchservice/CI)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/lavaswimmer/dandanplaysearchservice/latest)
![Docker Pulls](https://img.shields.io/docker/pulls/lavaswimmer/dandanplaysearchservice)

根据 [弹弹play资源搜索节点API规范](https://github.com/kaedei/dandanplay-libraryindex/blob/master/api/ResourceService.md) 开发的服务端API，支持docker。

# 部署

## 直接运行

```bash
git clone https://github.com/LandonLi/DanDanPlaySearchService.git
cd DanDanPlaySearchService
chmod +x ./install.sh
chmod +x ./start_local.sh
./install.sh
./start_local.sh
```

## 使用docker

### Play with Docker

[![Try in Play with Docker](https://raw.githubusercontent.com/play-with-docker/stacks/master/assets/images/button.png)](https://labs.play-with-docker.com/?stack=https://raw.githubusercontent.com/LandonLi/DanDanPlaySearchService/master/docker-compose.yml)

### 或者docker-compose

```bash
wget https://raw.githubusercontent.com/LandonLi/DanDanPlaySearchService/master/docker-compose.yml
docker-compose up -d
```

### 或者docker-cli

```bash
docker pull lavaswimmer/dandanplaysearchservice:latest
docker run -d -p 9145:9145 --name ddpss lavaswimmer/dandanplaysearchservice
```

# 使用

在弹弹play的`设置->网络与更新->自定义端点->修改资源搜索节点地址`框中输入地址`http://服务器的ip:9145`

# *其它

在国内的网络环境中`docker build`时，可以在`Dockerfile`中`RUN`部分替换alpine镜像地址，示例如下

```
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories && \
    apk add --update --no-cache --virtual .build-deps gcc libc-dev libxslt-dev && \
    apk add --no-cache libxslt && \
    pip3 install --no-cache-dir -r /app/requirements.txt && \
    apk del .build-deps
```