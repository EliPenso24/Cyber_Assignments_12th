# MD5 Brute Force

A distributed MD5 brute-force search over a TCP server and clients.

- `MD5_server.py`: asks for a number, pads it to 10 digits and computes its MD5 hash as the target. It listens on 127.0.0.1:65432 and gives each connected client a numeric range of 500,000 numbers per client CPU core. It stops the clients when a match is reported.
- `MD5_client.py`: connects to the server, requests work, and splits its range across one thread per CPU core. It hashes each number (padded to 10 digits) and reports `FOUND` with the number when the hash matches.

Run `MD5_server.py` first, then one or more `MD5_client.py`.
