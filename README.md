Basic uno card playing game
===========================

Hi! This project was created on an afternoon during a python course.
It features a client-server communication using XMLRPC and is written in python.
It neither includes authentication nor other security features, so do not host it publicly.

## How to use
1. Have atleast Python 3.5-ish installed
2. Use `git clone https://github.com/mheuwes/XMLRPC-Uno.git` to clone this project
3. `cd XMLRPC-uno` to go into the repo
4. Start a server using `python3 -m uno --server`, optionally giving a hostname/interface to listen on using `--host <host>` and/or a port to listen on using `--port <port>`
5. Connect all clients using `python3 -m uno --client`, with `--host <host>` and `--port <port>` if changed
6. Start the game using any key.
7. Enjoy!
8. `CTRL+C` to quit the game after the last round

## Known problems:
 - No default settings written in help
 - Help is not called automatically on no parameter
 - If a game is started using more than 2 players and one player is already finished, he is still in the game
