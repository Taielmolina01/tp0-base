testing_network="tp0_testing_net"
docker run --rm --network "$testing_network" alpine sh -c '
apk add --no-cache netcat-openbsd &&
message="hola"
success_message="action: test_echo_server | result: success"
fail_message="action: test_echo_server | result: fail"
echo_response=$(echo "$message" | nc -w 2 server 12345) &&
if [ "$echo_response" = "$message" ]; then 
    echo "$success_message" 
else
    echo "$fail_message"
fi
'