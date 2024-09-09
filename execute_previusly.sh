my_path=$(pwd)

wppconnect_path="/root/wppconnect-server"

cd $wppconnect_path

docker-compose stop
docker-compose up -d

cd $my_path


