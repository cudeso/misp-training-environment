# misp-training-environment

Goal: have a training environment where users can be Site and Org admin, alter MISP settings and play around with the MISP features. Restore the "playground" on a daily basis, without user interaction.

## MISP-cloud

The training environment is based on [MISP-cloud](https://github.com/MISP/misp-cloud) and the OSINT feed from [botvrij.eu](https://botvrij.eu/data/feed-osint/)

## Approach

1. Install MISP-cloud (AWS)
1. Change basic credentials and API keys. Run system update.
1. Change MISP URL and basic settings. 
1. Change auditing features of MISP to include client_ips in the logs
1. Update rsyslog to seperate misp logs from 'normal syslog
1. Configure the OSINT feed
1. Add demo users and demo organization
1. Truncate the logs (via mysql)
1. Create a backup with misp-backup
1. Create a cron job to restore the backup daily
1. Ship logs to external log collector
1. Enable Cloudlfare

The restore resets all changes done by the users in the demo environment, including MISP system configuration changes. It **does not** restore the users. This allows the demo users to remain access, after the restore has happened.

The script misp-restore-botvrij.sh is slightly altered compared to the original misp-restore. If does not require user-input (it can run from cron) and contains the Mysql root username.

## Cron-job

    30 6	* * *   root    /var/www/MISP/tools/misp-backup/misp-restore-botvrij.sh /opt/mispbackups/MISP-Backup-clean.tar.gz



