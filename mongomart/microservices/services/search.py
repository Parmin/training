import bottle




bottle.debug(True)
# Start the webserver running and wait for requests
bottle.run(host='localhost', port=8080)
