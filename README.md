## Python Chat Server and JavaScript Client using Websockets

### How to Use:

1. Activate the virtual environment. It already contains all the dependencies. On macOS, you can activate it using: `source venv/bin/activate`.

2. Start the Python server. You can use the command `python3 websocket.py`.

3. Open the HTML file in a web browser. Don't use any server to open it (like node.js), otherwise, it will give an error that it can't connect to the websocket directly. Instead, go to the file and open it with a web browser.

4. On the webpage, add a username and click on connect. You will see both the server and chat page interacting with each other.

### Learnings:

This project was a great learning experience for me. I got exposed to asynchronous programming in Python and did quite a bit of reading to properly understand how the asyncio library works in Python. A major resource that helped me was [Superfast Python](https://superfastpython.com/python-asyncio/), in addition to a bunch of YouTube videos and official documentation.

Asynchronous programming also got me intrigued about its comparison with Goroutines, JavaScript event loop, and what exactly differentiates it from threading and multiprocessing.

I used the websocket library from Python in a typical asynchronous fashion. I made the console input an async function to accept prompts from the console. After reading deeper into asynchronous programming, it didn't take much time to write code that uses websockets.

### Further Improvement:

1. This project could definitely be made much better and fancier. But my aim here was to just explore the workings of sockets, integrating JavaScript, Python, HTML, and CSS together, understanding its working, code flow, etc.
2. If I have time in the future, I would love to use all these learnings and simply create a simple chat application.

---
