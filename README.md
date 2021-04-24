# Simba Coins

<p align="center">
  <img src="https://img.shields.io/static/v1?label=python&message=3.9.1&color=blue&style=for-the-badge&logo=python"/>
</p>

## Summary

- [Overview](#overview)
- [Requirements](#requirements)
- [How to run](#how-to-run)
- [Todo](#todo)
- [Authors](#authors)

## Overview

This project uses sockets and threads.

The communication protocol is based on request/response, which for any request from the client, the server returns a response, performing the appropriate actions for specific requests.

The client connects to the server socket, and be able to send and receive structured (and standardized) messages using the `pickle` library.

The server starts a Thread for each client connected at the address it is listening to, handling its connection and offering the client three states (with different requests available, handling requests not available for each state).

The state control was implemented using the [`State Design Pattern`](https://refactoring.guru/design-patterns/state).

## Requirements

Only need Python 3.9.1 installed :)

## How to run

First, the server needs to be started.\
In the terminal, open the project folder and run the command:

```
python server\server.py
```

Then, as many clients as needed can be started.\
Open another terminal in the project folder and run the command (for each client):

```
python client\client.py
```

## Todo
- [x] Configure repo
- [x] Create a readme
- [] Regularize imports
- [] Create a shell-script-based file to run the project with just one command

## Authors
- [paulowsky](https://github.com/paulowsky)
