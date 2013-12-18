# must run in root, at project_dir

# install basic packages
apt-get install python-virtualenv build-essential lighttpd

# copy configure file
cp ./utils/lighttpd/lighttpd.conf /etc/lighttpd/
cp ./utils/django-servers.sh /etc/init.d/
chmod +x /etc/init.d/django-servers.sh
# backup
cp ./utils/backup/dropbox /etc/init.d/
cp ./utils/backup/backup.py /etc/cron.daily/
chmod +x /etc/init.d/dropbox
chmod +x /etc/cron.daily/backup.py

# enalbe services at bootup
update-rc.d -f django-servers.sh defaults
update-rc.d django-servers.sh enable
update-rc.d -f lighttpd defaults
update-rc.d lighttpd enable
update-rc.d -f dropbox defaults
update-rc.d dropbox enable
service cron restart
