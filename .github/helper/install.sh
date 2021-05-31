#!/bin/bash

set -e

cd ~ || exit

sudo apt-get install redis-server

sudo apt install nodejs

sudo apt install npm

pip install vmraid-bench

git clone https://github.com/vmraid/vmraid --branch "${GITHUB_BASE_REF:-${GITHUB_REF##*/}}" --depth 1
bench init --skip-assets --vmraid-path ~/vmraid --python "$(which python)" vmraid-bench

mkdir ~/vmraid-bench/sites/test_site
cp -r "${GITHUB_WORKSPACE}/.github/helper/site_config.json" ~/vmraid-bench/sites/test_site/

mysql --host 127.0.0.1 --port 3306 -u root -e "SET GLOBAL character_set_server = 'utf8mb4'"
mysql --host 127.0.0.1 --port 3306 -u root -e "SET GLOBAL collation_server = 'utf8mb4_unicode_ci'"

mysql --host 127.0.0.1 --port 3306 -u root -e "CREATE USER 'test_vmraid'@'localhost' IDENTIFIED BY 'test_vmraid'"
mysql --host 127.0.0.1 --port 3306 -u root -e "CREATE DATABASE test_vmraid"
mysql --host 127.0.0.1 --port 3306 -u root -e "GRANT ALL PRIVILEGES ON \`test_vmraid\`.* TO 'test_vmraid'@'localhost'"

mysql --host 127.0.0.1 --port 3306 -u root -e "UPDATE mysql.user SET Password=PASSWORD('travis') WHERE User='root'"
mysql --host 127.0.0.1 --port 3306 -u root -e "FLUSH PRIVILEGES"

wget -O /tmp/wkhtmltox.tar.xz https://github.com/vmraid/wkhtmltopdf/raw/master/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
tar -xf /tmp/wkhtmltox.tar.xz -C /tmp
sudo mv /tmp/wkhtmltox/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf
sudo chmod o+x /usr/local/bin/wkhtmltopdf
sudo apt-get install libcups2-dev

cd ~/vmraid-bench || exit

sed -i 's/watch:/# watch:/g' Procfile
sed -i 's/schedule:/# schedule:/g' Procfile
sed -i 's/socketio:/# socketio:/g' Procfile
sed -i 's/redis_socketio:/# redis_socketio:/g' Procfile

bench get-app erpadda "${GITHUB_WORKSPACE}"
bench start &
bench --site test_site reinstall --yes
