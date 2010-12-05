/**
 * Part of the AONIC Framework.
 * 
 * Used as a middle layer between the Push Communication framework and server side daemon.
 *
 * @author Raja Kapur
 * @link http://framework.aonic.net/
 * @see AONIC.Com.js
 */
System.security.allowDomain("*");

var jsAPI = new Object();
jsAPI._instanceId = 0;
jsAPI.log = function(msg) {
	flash.external.ExternalInterface.call("AONIC.log", "[" + this._instanceId + "] ", msg);
}
jsAPI.l = function(method) {
	return "AONIC.instances[" + this._instanceId + "]." + method;
}

jsAPI.log("Flash loading");

var process = new XMLSocket();
process.onConnect = function(success) {
    jsAPI.log("Connected to server: " + success);
    flash.external.ExternalInterface.call(jsAPI.l("_onConnect"), success);
};
process.onClose = function() {
    jsAPI.log("Connection to server closed");
    flash.external.ExternalInterface.call(jsAPI.l("_onClose"));
};
process.onData = function(line) {
    jsAPI.log("Received data: " + line);
    if (line) flash.external.ExternalInterface.call(jsAPI.l("_onData"), line.split("\\").join("\\\\"));
};

flash.external.ExternalInterface.call(jsAPI.l("setStatus"), 'connected', true);

var jsInterface = new Object();
jsInterface.connect = function(server, port, instanceId) {
	jsAPI._instanceId = instanceId;
    jsAPI.log("Connecting to: " + server + ":" + port);
    //System.security.loadPolicyFile("http://" + server + ":" + port + "/crossdomain.xml");
    System.security.loadPolicyFile("xmlsocket://" + server + ":" + port + "");
    jsAPI.log("xmlsocket://" + server + ":" + port + "");
    process.connect(server, port);
};
jsInterface.send = function(line) {
    jsAPI.log("Sending data: " + line);
    process.send(line);
};
jsInterface.close = function() {
    jsAPI.log("Closing connection");
    process.close();
};

flash.external.ExternalInterface.addCallback("_close", jsInterface, jsInterface.close);
flash.external.ExternalInterface.addCallback("_send", jsInterface, jsInterface.send);
flash.external.ExternalInterface.addCallback("_connect", jsInterface, jsInterface.connect);