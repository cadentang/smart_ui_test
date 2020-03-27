cd /d %~dp0
cd ..
cd extend
start java -jar selenium-server-standalone-3.9.1.jar -role hub -port 4444
start java -jar selenium-server-standalone-3.9.1.jar -role node -port 5555 -hub http://192.168.124.10:4444/grid/register
start java -jar selenium-server-standalone-3.9.1.jar -role node -port 5556 -hub http://192.168.0.141:4444/grid/register