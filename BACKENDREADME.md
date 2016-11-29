### HOW TO RUN THE SERVER
** TO START NGINX: **
sudo /etc/rc.d/init.d/nginx start
** TO STOP NGINX: **
sudo /etc/rc.d/init.d/nginx stop
** TO LIST GUNICORN PROCESSES: **
ps ax|grep gunicorn
** TO KILL GUNICORN PROCESSES: **
pkill gunicorn
** TO RUN GUNICORN PROCESSES: **
gunicorn VariationsBackend:app -b localhost:8000 &
** IN ORDER TO SERVE APP WITH DEV SERVER (NOT RECOMMENDED) **
Enter tmux with tmux
In tmux, sudo python VariationsBackend.py
Detach from tmux with ctrl + B followed by D
