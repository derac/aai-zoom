var socket = io.connect("http://" + document.domain + ":" + location.port);
var translation_output = document.querySelector("#translation_output");
var start_button = document.querySelector("#start_button");
var zoom_link = document.querySelector("#zoom_link");

socket.on("connect", function () {
  console.log("connected");
});
socket.on("data", function (data) {
  console.log(data);
  var message_text = document.createTextNode(data);
  var line_break = document.createElement("br");
  translation_output.appendChild(message_text);
  translation_output.appendChild(line_break);
});
start_button.addEventListener("click", () => {
  console.log(zoom_link.value);
});

setInterval(() => {
  socket.emit("message", "test");
}, 500);
