!/bin/bash
export DISPLAY=:1
source /home/admin/Desktop/tighvnc/venv/bin/activate
sleep 5 # Espera 5 segundos
xhost +si:localuser:$USER
python /home/admin/Desktop/tighvnc/main.py
xhost -si:localuser:$USER
deactivate
exit 0
