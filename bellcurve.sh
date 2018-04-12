# python3 client/http_client.py 10.1.0.138 10 1 & PID=$!
# sleep 1m
# kill -HUP $PID

# python3 client/http_client.py 10.1.0.138 10 0.5 & PID=$!
# sleep 2m
# kill -HUP $PID

# python3 client/http_client.py 10.1.0.138 15 0.5 & PID=$!
# sleep 2m
# kill -HUP $PID

# python3 client/http_client.py 10.1.0.138 10 0.5 & PID=$!
# sleep 2m
# kill -HUP $PID

# python3 client/http_client.py 10.1.0.138 10 1 & PID=$!
# sleep 1m
# kill -HUP $PID


python3 client/http_client.py 10.1.0.138 10 1 & PID=$!
sleep 30s
kill -HUP $PID

python3 client/http_client.py 10.1.0.138 10 0.5 & PID=$!
sleep 1m
kill -HUP $PID

python3 client/http_client.py 10.1.0.138 15 0.5 & PID=$!
sleep 1m
kill -HUP $PID

python3 client/http_client.py 10.1.0.138 10 0.5 & PID=$!
sleep 1m
kill -HUP $PID

python3 client/http_client.py 10.1.0.138 10 1 & PID=$!
sleep 30s
kill -HUP $PID
