sleep 5
cd /home/ipt/cimento/
python main.py &
sleep 5
chromium-browser --kiosk "0.0.0.0:5000"
