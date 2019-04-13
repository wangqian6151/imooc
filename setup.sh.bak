#!/usr/bin/env bash

# 如何使用
# sudo -E bash -x setup_development.sh

# ${source_root} 是代码所在目录
source_root='/root/web21'


# 换成中科大的源
sudo ln -f -s ${source_root}/sources.list /etc/apt/sources.list
sudo mkdir /root/.pip
sudo ln -f -s ${source_root}/pip.conf /root/.pip/pip.conf

# 装依赖
sudo apt-get update
sudo apt-get install -y git python3 python3-pip
sudo apt-get install -y nginx mongodb supervisor redis-server apache2-utils

sudo pip3 install -U pip setuptools wheel
sudo pip3 install jinja2 flask gunicorn pymongo gevent redis

# 删掉 nginx default 设置
sudo rm -f /etc/nginx/sites-enabled/*
sudo rm -f /etc/nginx/sites-available/*

# 建立一个软连接
sudo ln -s -f ${source_root}/web21.conf /etc/supervisor/conf.d/web21.conf
# 不要再 sites-available 里面放任何东西
sudo ln -s -f ${source_root}/web21.nginx /etc/nginx/sites-enabled/web21

# 设置文件夹权限给 nginx 用
sudo chmod o+xr /root
sudo chmod -R o+xr ${source_root}

sudo service supervisor restart
sudo service nginx restart

echo "setup development environemtn success"