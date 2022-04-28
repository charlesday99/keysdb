post_to_keysdb () {
        curl -X POST -H "Content-Type: application/json" -d '{"value":"'"$2"'"}' "https://db.charlieday.dev/key/$1"
}

# A tool to update the KeysDB with your interal & external IP
# Example cron job:
#
# 3 AM: Update shared IP
# 0 3 * * * /var/www/keysdb/tools/share_ip.sh

post_to_keysdb "$(hostname)-external" "$(curl ipinfo.io/ip)"
post_to_keysdb "$(hostname)-internal" "$(hostname -I | awk '{print $1}')"
