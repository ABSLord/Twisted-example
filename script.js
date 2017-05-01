/**
 * Created by Antonio on 02.05.2017.
 */
var webSocket;
var port = "12345";
function addLog(s) {
    var log = document.getElementById("log");
    log.value = s + "\n----------------------------------------------------------\n" + log.value;
}
function connect()  {
    webSocket = new WebSocket("ws://127.0.0.1:" + port);
    webSocket.onopen = function() {
          addLog("Connection is established!");
    };
    webSocket.onclose = function() {
      addLog("Connection is broken!");
    };
    webSocket.onerror = function(error) {
        addLog("Error " + error.message);
    };
    webSocket.onmessage = function(event) {
        addLog("Answer received: " + event.data);
    };
}
function disconnect() {
    if (typeof webSocket == "undefined") {
        alert("You are not connected to the web socket server!");
        return;
    }
    webSocket.close()
}

function createRequest(button){
    var password = document.getElementById("password").value;
    var name = document.getElementById("name").value;
    return button.toString() + ":" + name.toString() + "&" + password.toString();
}
function check() {
    if (typeof webSocket == "undefined" || webSocket.readyState == webSocket.CLOSED) {
        alert("You are not connected to the web socket server!");
        return;
    }
    var result = createRequest("check");
    webSocket.send(result);
    addLog("Request has been sent: " + result);
}
function login() {
    if (typeof webSocket == "undefined" || webSocket.readyState == webSocket.CLOSED) {
        alert("You are not connected to the web socket server!");
        return;
    }
    var result = createRequest("login");
    webSocket.send(result);
    addLog("Request has been sent: " + result);
}
function add() {
    if (typeof webSocket == "undefined" || webSocket.readyState == webSocket.CLOSED) {
        alert("You are not connected to the web socket server!");
        return;
    }
    var result = createRequest("add");
    webSocket.send(result);
    addLog("Request has been sent: " + result);
}
function logout() {
    if (typeof webSocket == "undefined" || webSocket.readyState == webSocket.CLOSED) {
        alert("You are not connected to the web socket server!");
        return;
    }
    var result = createRequest("logout");
    webSocket.send(result);
    addLog("Request has been sent: " + result);
}
