# GOT Hybrid Encryption

"Game of Thrones: The White Wolf", a 2-player cooperative maze game over TCP with hybrid encryption.

- `GOT_server.py`: listens on port 5555 and accepts exactly 2 players. It runs the game logic, collisions, artifact collection, a dragon that chases the players with BFS pathfinding, and the win/lose conditions. It sends the full game state to both clients after every update.
- `GOT_client (1).py`: the pygame client with Home, Narrative, Waiting, Gameplay and End screens. It connects to 127.0.0.1:5555, sends movement (arrow keys or WASD) and draws the state it receives.

Encryption: on connect, the server sends its RSA public key, the client sends back a Fernet key encrypted with it (RSA-OAEP), and all game messages after that are encrypted with Fernet.

Imports: `pygame` (client) and `cryptography`. Start the server first, then both clients.
