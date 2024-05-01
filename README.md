[![CodeFactor](https://www.codefactor.io/repository/github/landonli/ddpss/badge)](https://www.codefactor.io/repository/github/landonli/ddpss)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/landonli/ddpss/main.yml?branch=master)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/1andonli/ddpss/latest)
![Docker Pulls](https://img.shields.io/docker/pulls/1andonli/ddpss)

根据 [弹弹play资源搜索节点API规范](https://github.com/kaedei/dandanplay-libraryindex/blob/master/api/ResourceService.md) 开发的服务端API，支持docker。

# 部署

## 直接运行

```bash
git clone https://github.com/LandonLi/ddpss.git
cd ddpss
chmod +x ./install.sh
chmod +x ./start_local.sh
./install.sh
./start_local.sh
```

## 使用docker

### docker-compose

```bash
wget https://raw.githubusercontent.com/LandonLi/ddpss/master/docker-compose.yml
docker-compose up -d
```

### docker-cli

```bash
docker pull 1andonli/ddpss:latest
docker run -d -p 9145:9145 --name ddpss 1andonli/ddpss:latest
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
