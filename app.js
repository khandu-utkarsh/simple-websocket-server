// import { startChatting } from "chatModule.js";

"use strict";
const host = document.location.hostname;
const port = document.location.port;

let socket;

function startChatting(e) {
  e.preventDefault();
  const username = document.getElementById("username").value;
  const connectForm = document.getElementById("connect-form");
  const chatApp = document.getElementById("chat-app");

  connectForm.style.display = "none";

  const status = document.getElementById("status");
  const chats = document.getElementById("chats");

  status.innerHTML = "Connecting...";
  status.className = "connecting";

  socket = new WebSocket("ws://127.0.0.1:8000");

  socket.onopen = () => {
    status.innerHTML = "Connected";
    status.className = "connected";
    chatApp.style.display = "block";
    sendMessage({
      type: "new_user",
      username,
    });
  };

  socket.onmessage = (response) => {
    const tr = document.createElement("tr");
    const message_received = response.data;
    //const data = JSON.parse(response.data);
    console.log(message_received);
    // if (data.type === "notice") {
    //   data.username = "*Server Message*";
    // }
    //tr.innerHTML = `<td>${data.datetime}</td><td>${data.username}</td><td>${data.message}</td>`;
    tr.innerHTML = `${message_received}`;
    chats.appendChild(tr);
  };

  function handleInput(e) {
    e.preventDefault();
    const chatInput = document.getElementById("enter-chat");
    sendMessage({
      type: "user_message",
      message: chatInput.value,
    });
    chatInput.value = "";
  }

  const submit = document.getElementById("submit");
  submit.addEventListener("click", handleInput);
  const myForm = document.getElementById("my-form");
  myForm.addEventListener("submit", handleInput);
}

function sendMessage(data) {
  socket.send(JSON.stringify(data));
}

window.onload = () => {
  const startChatForm = document.getElementById("start-chat-form");
  startChatForm.addEventListener("submit", startChatting);
};

// window.addEventListener("DOMContentLoaded", () => {
//   const messages = document.createElement("ul");
//   document.body.appendChild(messages);

//   const websocket = new WebSocket("ws://127.0.0.1:8000");
//   websocket.onmessage = ({ data }) => {
//     const message = document.createElement("li");
//     const content = document.createTextNode(data);
//     message.appendChild(content);
//     messages.appendChild(message);
//   };
// });

// function startSocket() {
//   var ws = new WebSocket("ws://127.0.0.1:8000");
//   ws.onopen = function (event) {
//     ws.send("Sent this from client.js");
//   };
// }
// startSocket();
