okay so there are 3 problems i am facing here:
this error message is being shown in websocketserver :
Traceback (most recent call last):
  File "c:\Users\devgo\Documents\GitHub\Dynamic-Leaderboard-\.venv\Lib\site-packages\websockets\legacy\server.py", line 245, in handler
    await self.ws_handler(self)
  File "c:\Users\devgo\Documents\GitHub\Dynamic-Leaderboard-\.venv\Lib\site-packages\websockets\legacy\server.py", line 1190, in _ws_handler
    return await cast(
           ^^^^^^^^^^^
  File "C:\Users\devgo\Documents\GitHub\Dynamic-Leaderboard-\flask-leaderboard\websocketserver.py", line 25, in leaderboard_update
    await broadcast_to_clients(data)
  File "C:\Users\devgo\Documents\GitHub\Dynamic-Leaderboard-\flask-leaderboard\websocketserver.py", line 36, in broadcast_to_clients
    await asyncio.wait([client.send(message) for client in connected_clients])
  File "C:\Users\devgo\AppData\Local\Programs\Python\Python312\Lib\asyncio\tasks.py", line 461, in wait
    raise TypeError("Passing coroutines is forbidden, use tasks explicitly.")
TypeError: Passing coroutines is forbidden, use tasks explicitly.
this error is being shown to the client:
Connected to server at ws://localhost:8765
Data sent to the server: {'player_id': 'Player_86', 'score': 2476}
Connection closed with error: received 1011 (internal error); then sent 1011 (internal error)
and when i go to my website and add the score the scores are not being added and the updated table is not shown in my screen