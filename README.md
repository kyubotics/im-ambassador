# IM Ambassador

[![License](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://github.com/richardchien/im-ambassador/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/richardchien/im-ambassador.svg?branch=master)](https://travis-ci.org/richardchien/im-ambassador)
[![Docker Repository](https://img.shields.io/badge/docker-richardchien%2Fim--ambassador-blue.svg)](https://hub.docker.com/r/richardchien/im-ambassador/)

这是从 [CCZU-DEV/xiaokai-bot](https://github.com/CCZU-DEV/xiaokai-bot) 精简而来的即时聊天消息转发器。

名字的「Ambassador」意为「使者」，「IM」意为「即时聊天」，也可理解为「我是」，寓意这个 bot 在多个即时聊天平台承担使者的角色，按某一既定规则转发、回复消息。

转发规则可通过配置文件设置，自定义性比较强。另外，消息发送器采用适配器模式，易于扩展不同的 IM 平台。目前仅支持接收和发送基于 [sjdy521/Mojo-Webqq](https://github.com/sjdy521/Mojo-Webqq) 和 [sjdy521/Mojo-Weixin](https://github.com/sjdy521/Mojo-Weixin) 的消息。

## 使用场景

- 将多个小号收到的消息转发到大号，并在大号里直接回复
- 将微信收到的消息转发到 QQ，并在 QQ 里直接回复
- 仅将某几个群的包含某几个关键词的消息转发到另一个账号
- 对同一个社区在不同平台的分群消息进行互相转发
- 更多使用场景等待你发现……

## 快速开始

### 预备

由于目前只支持 [sjdy521/Mojo-Webqq](https://github.com/sjdy521/Mojo-Webqq) 和 [sjdy521/Mojo-Weixin](https://github.com/sjdy521/Mojo-Weixin) 这两个消息源，因此你可能需要首先去了解如果使用它们来登录你的 QQ 或微信账号。

另外本项目需要 Python 3.x，下面的命令可能要换成 `pip3`、`python3`。

### 修改配置文件

复制 `config.sample.json` 为 `config.json` 或复制 `config.sample.py` 为 `config.py`（两者有任意一个即可），然后按需进行修改，具体写法见 [配置文件写法](https://github.com/richardchien/im-ambassador/wiki/%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%E5%86%99%E6%B3%95)。

### 运行程序

首先安装依赖：

```sh
pip install -r requirements.txt
```

然后启动程序：

```sh
python app.py

# 或

python app.py 9000

# 或

python app.py 127.0.0.1 8080
```

不加参数会默认监听 `0.0.0.0:8080`，加参数可以自定 IP 和端口。这两个参数也可以分别通过环境变量 `IM_AMBASSADOR_HOST` 和 `IM_AMBASSADOR_PORT` 来设置。

### 在 Docker 中运行程序

相比起直接运行，使用 Docker 来运行本程序是一种更方便快捷的方法，例如下面启动命令：

```sh
docker run -ti --rm -e "IM_AMBASSADOR_HOST=0.0.0.0" -e "IM_AMBASSADOR_PORT=9000" -v config.json:config.json --name my-im-ambassador richardchien/im-ambassador
```

### 设置消息源的上报地址

无论什么消息源，都需要通过 HTTP POST 来将收到的消息以 JSON 的形式发送给本程序。

为了区分不同的消息源，设置上报地址时需要对不同的消息源指定不同的子路径。对于现在支持的 sjdy521/Mojo-Webqq 和 sjdy521/Mojo-Weixin，分别提供了 `/qq/` 和 `/wx/` 两个子路径，且由于微信的特殊性（经常获取不到消息接收者的账号），另外提供了 `/wx/<string:account>` 来强制指定来源账号（对于消息源来说，也就是它所登录的账号）。

例如，如果你使用 sjdy521/Mojo-Weixin 作为消息源登录微信号 your_wechat_id，并且运行本程序的时候监听了 `127.0.0.1:8888`，那么你需要在运行 sjdy521/Mojo-Weixin 时指定上报地址为 `http://127.0.0.1:8888/wx/your_wechat_id`。

## 更多配置

项目中给出的 `config.sample.json` 中是一种非常简单的配置，你可以参考 [配置文件写法](https://github.com/richardchien/im-ambassador/wiki/%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%E5%86%99%E6%B3%95) 来进行你自己的定制，也可以参考 [配置文件示例](https://github.com/richardchien/im-ambassador/wiki/%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%E7%A4%BA%E4%BE%8B) 给出的几种典型的使用场景下的配置文件。
