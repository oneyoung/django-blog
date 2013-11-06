# must run in root, at project_dir

# install basic packages
apt-get install python-virtualenv build-essential lighttpd

# copy configure file
cp ./utils/lighttpd/lighttpd.conf /etc/lighttpd/
cp ./utils/django-servers.sh /etc/init.d/
chmod +x /etc/init.d/django-servers.sh

# enalbe services at bootup
update-rc.d -f django-servers.sh defaults
update-rc.d django-servers.sh enable
update-rc.d -f lighttpd defaults
update-rc.d lighttpd enable
