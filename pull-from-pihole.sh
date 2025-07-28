ssh  <pi_usr>@<pi_local_ip> \
"sudo /usr/bin/sqlite3 /etc/pihole/pihole-FTL.db \
\"SELECT DISTINCT 'https://' || domain FROM queries WHERE timestamp > strftime('%s','now','-6 months') ORDER BY domain;\"" \
> </path/to>/obsfucation-container/websites.txt

