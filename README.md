# GStreamer_singlecamera
```
sudo chmod a+x /home/pi/GStreamer_singlecamera/startCamera.sh
```
```
sudo nano /etc/rc.local
```
Add the following line before end
```
/home/pi/GStreamer_singlecamera/startCamera.sh &
```
# Python version
1. 新版的gplayer.py可以直接執行，但是要先下載依賴的函式庫
2. 修改程式碼內的船名和地面站的名字，要對應到地面站GPlayer程式內的設定
```
BOAT_NAME = '船名'
GROUND_NAME = '地面站名'
```
