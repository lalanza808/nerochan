# nerochan

Post your best neroChans. Get tipped.

No middle-men. p2p tips.

No passwords. Wallet signing authentication.

## Setup

This install guide was written for Ubuntu.

Launch a new VPS and point a domain of your choice to it. I'll refer to said domain as `$DOMAIN` below.

```
# Update package list
apt update

# Install web server, tools, and system libraries
apt install nginx python3-venv certbot python3-certbot-nginx docker.io docker-compose make

# Note - If you don't want to run Docker, you can just install/run monero-wallet-rpc and background it instead

# Remove default Nginx config
rm /etc/nginx/sites-enabled/default

# Add http Nginx config
vim /etc/nginx/sites-enabled/nerochan.conf
<<<
server {
    listen 80;
    server_name nerochan-test.suchwow.xyz;
    error_log /var/log/nginx/nerochan-test.suchwow.xyz-error.log warn;
    access_log /var/log/nginx/nerochan-test.suchwow.xyz-access.log;
    client_body_in_file_only clean;
    client_body_buffer_size 32K;
    client_max_body_size 30M;
    sendfile on;
    send_timeout 600s;

    location / {
        proxy_pass http://127.0.0.1:4000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Frame-Options "SAMEORIGIN";
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Cookie $http_cookie;
        proxy_redirect off;
    }
}
>>>

# Configure SSL for web server - certbot will inject SSL config into your above nerochan.conf
certbot --nginx -d $DOMAIN --agree-tos -m $YOUR_EMAIL

# Create new user for running app
useradd -m -G docker -s /bin/bash nerochan   # omit docker group if running without it

# sudo into nerochan user
sudo -u nerochan bash
cd ~/

# Clone the repo
git clone https://github.com/lalanza808/nerochan

# Setup secrets
cp env-example .env

# Build and run monero-wallet-rpc
make up   # uses docker-compose to build a container image which runs ./bin/run_wallet.sh (monero-wallet-rpc)

# Install Python dependencies for Flask app
make setup

# Initialize the database based on nerochan/models.py (default goes to ./data/sqlite.db)
make init

# Run Gunicorn production web service
make prod

# Register new user on the site

# Make user an admin via CLI
./manage.py add_admin $HANDLE
```

If everything worked as intended, you should have Gunicorn running in the background on port 4000 as `nerochan` user, with Nginx config accepting requests for your $DOMAIN, proxying requests to Gunicorn. You'll have a SQLite database keeping all the relational app data somewhere you've defined (default is app repo ./data/sqlite.db), and a filesystem for future uploads from your artists. You'll have an administrator within the application's /admin interface for managing the system.

To process tips, run the following (setup a cron task):

```
./manage.py verify_tips
```


## Dev Stuff

Stagenet txes for testing/validation:

| recipient | tx_id | tx_key |
| --- | ---  | --- |
| 78TanhCTvw4V8HkY3vD49A5EiyeGCzCHQUm59sByukTcffZPf3QHoK8PDg8WpMUc6VGwqxTu65HvwCUfB2jZutb6NKpjArk | 077b8654dd95fdfbd6d97808e2a9ad37cf767fb2f9da4cb0e1e6427c8587f6ee | be64bd151bd01cb4f8572a3c9731d0dff726079213e9f7017957799edc46630b |
| 78TanhCTvw4V8HkY3vD49A5EiyeGCzCHQUm59sByukTcffZPf3QHoK8PDg8WpMUc6VGwqxTu65HvwCUfB2jZutb6NKpjArk | 46fd71389ed54f195d359b84897bb89b37bb8da0bbe72ef22b552c8786346805 | b683e96770c76a1a23253873ad8a2ebb1832e14d90a05fb49a9e6e22e73d630a |
|  |  |  |