# misp-training-environment

Goal: have a training environment where users can be Site and Org admin, alter MISP settings and play around with the MISP features. Restore the "playground" on a daily basis, without user interaction.

## MISP-cloud

The training environment is based on [MISP-cloud](https://github.com/MISP/misp-cloud) and the OSINT feed from [botvrij.eu](https://botvrij.eu/data/feed-osint/)

## Approach

1. Install MISP-cloud (AWS)
1. Change basic credentials and API keys. Run system update.
1. Change MISP URL and basic settings. 
1. Change auditing features of MISP to include client_ips in the logs
1. Update rsyslog to seperate misp logs from 'normal' syslog
1. Configure the OSINT feed
1. Add demo users and demo organization
1. Truncate the logs (via mysql)
1. Create a backup with misp-backup
1. Create a cron job to restore the backup daily
1. Ship logs to external log collector
1. Enable Cloudflare

The restore resets all changes done by the users in the demo environment, including MISP system configuration changes. It **does not** restore the users or remove new created users/organisations. This allows demo users to keep access with their newly created users (and API keys), after the restore has happened. Cleanup of demo users (and organisations) is a manual action.

The script misp-restore-botvrij.sh is slightly altered compared to the original misp-restore. If does not require user-input (it can run from cron) and contains the Mysql root username.

## Cron-job

    30 6	* * *   root    /var/www/MISP/tools/misp-backup/misp-restore-botvrij.sh /opt/mispbackups/MISP-Backup-clean.tar.gz

# MISP and a webshell via web interface

Install **ShellInABox** and edit the config file.

```
sudo apt install openssl shellinabox
sudo vi /etc/default/shellinabox
```

Add these settings to have ShellInABox listen on the localhost and connect to a local system. Replace `192.168.171.10` with the IP addresss of the host you'd like to connect to.

```
SHELLINABOX_ARGS="--no-beep --localhost-only"
OPTS="-s /:SSH:192.168.171.10"
```

Stop Apache and install **nginx** to be used as a reverse proxy and add a config file. Nginx will use the SSL password created for MISP.

```
sudo systemctl stop apache2
sudo apt-get install nginx
sudo /etc/nginx/sites-enabled/misp-template.conf
```

```
server {
    listen 80;
    return 301 https://$host$request_uri;
}

server{

 listen 443 ssl;
 ssl_certificate /etc/ssl/private/misp.local.crt;
 ssl_certificate_key /etc/ssl/private/misp.local.key;

 location /
 {
	 proxy_pass https://127.0.0.1:8443/;
	 proxy_redirect default;
	 proxy_set_header Host $host;
	 proxy_set_header X-Real-IP $remote_addr;
	 proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	 client_max_body_size 10m;
	 client_body_buffer_size 128k;
	 proxy_connect_timeout 90;
	 proxy_send_timeout 90;
	 proxy_read_timeout 90;
	 proxy_ssl_verify off;
	 proxy_buffer_size 4k;
	 proxy_buffers 4 32k;
	 proxy_busy_buffers_size 64k;
	 proxy_temp_file_write_size 64k;
 }
 location /shell/
 {
	 proxy_pass https://127.0.0.1:4200/;
	 proxy_redirect default;
	 proxy_set_header Host $host;
	 proxy_set_header X-Real-IP $remote_addr;
	 proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	 client_max_body_size 10m;
	 client_body_buffer_size 128k;
	 proxy_connect_timeout 90;
	 proxy_send_timeout 90;
	 proxy_read_timeout 90;
	 proxy_ssl_verify off;
	 proxy_buffer_size 4k;
	 proxy_buffers 4 32k;
	 proxy_busy_buffers_size 64k;
	 proxy_temp_file_write_size 64k;
 }
}
```

Then make sure you configure Apache to listen on 8443 and restart the web server.

```
vi /etc/apache2/ports.conf
```

```
Listen 8080

<IfModule ssl_module>
        Listen 8443
</IfModule>

<IfModule mod_gnutls.c>
        Listen 8443
</IfModule>
```

```
vi /etc/apache2/sites-enabled/misp-ssl.conf
```

```
<VirtualHost *:8443>
```

