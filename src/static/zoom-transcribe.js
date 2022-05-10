var socket = io.connect("http://" + document.domain + ":" + location.port);
var start_button = document.querySelector("#start_button");
var zoom_link = document.querySelector("#zoom_link");

var translation_output = document.querySelector("#translation_output");
var message_text;
function setup_translation_output() {
  translation_output.innerHTML = "";
  message_text = document.createElement("div");
  translation_output.appendChild(message_text);
  translation_output.appendChild(document.createElement("br"));
}
setup_translation_output();

start_button.addEventListener("click", () => {
  setup_translation_output();
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/transcribe", true);
  xhr.onload = function (e) {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        console.log(xhr.responseText);
      } else {
        console.error(xhr.statusText);
      }
    }
  };
  xhr.onerror = function (e) {
    console.error(xhr.statusText);
  };
  xhr.send(zoom_link.value);
});
socket.on("connect", function () {
  console.log("socketio connected");
});

socket.on("data", function (data) {
  data = JSON.parse(data);
  console.log(data);
  if (data["message_type"] == "PartialTranscript") {
    message_text.innerHTML = data["text"];
  } else {
    message_text.innerHTML = data["text"];
    message_text = document.createElement("div");
    translation_output.appendChild(message_text);
    translation_output.appendChild(document.createElement("br"));
  }
});
