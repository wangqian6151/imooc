#!/usr/bin/env bash

# 如何使用
# sudo -E bash -x setup_development.sh

# ${source_root} 是代码所在目录
source_root='/home/crawler/imooc'


# 装依赖
sudo apt-get update
sudo apt-get install -y git python3 python3-pip
sudo apt-get install -y nginx mongodb supervisor redis-server apache2-utils

sudo pip3 install -U pip setuptools wheel
sudo pip3 install jinja2 flask gunicorn pymongo gevent redis


# 建立一个软连接
sudo ln -s -f ${source_root}/imooc.conf /etc/supervisor/conf.d/imooc.conf


# 设置文件夹权限给 nginx 用
sudo chmod o+xr /root
sudo chmod -R o+xr ${source_root}

sudo service supervisor restart

echo "setup development environemtn success"