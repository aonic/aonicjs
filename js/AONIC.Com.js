/**
 * Beginnings of a AONIC Framework.
 * (c) 2007 - 2008 Raja Kapur <raja@aonic.net>
 * 
 * The AONIC Framework is freely distributable under the terms of the MIT License.
 * See http://framework.aonic.net/ for details.
 * 
 * @author Raja Kapur
 * @link http://framework.aonic.net/
 */
var AONIC = {
	instances: [0],
    config: {},
	api: {},
	debug: false,
	
	$: function(id) {
		return (document.getElementById(id) || false);
	},
	log: function() {
		if(!this.debug) return;
		
		if(window.console) console.log(arguments[0] + ' ' + arguments[1]);
		else alert(arguments[0] + ' ' + arguments[1]);
	}
};
// bind() concept from prototype.js (http://www.prototypejs.org), MIT (source code) license.
Function.prototype.bind = function() {
	if (arguments.length < 2 && arguments[0] === undefined) return this;
	var __method = this;
	var args = []; for(var i=0; i<arguments.length; i++) {
		args.push(arguments[i])
	}
	var object = args.shift();
	return function() {
    	return __method.apply(object, args);
	}
};

/**	
 * Basic JS effects library.
 * (c) 2007 - 2008 Raja Kapur <raja@aonic.net>
 *
 * @example
 * 	new AONIC.api.Effects('photoBox', 0, 300, 'height', {duration:300}).slide()
 *
 * @author Raja Kapur
 * @link http://framework.aonic.net/
 */
AONIC.api.Effects = function(el, start, end, property, options) {
	if(typeof(options) == "undefined") options = {};
	
	this.start = start;
	this.end = end;
	this.change = (end - start);
	this.duration = options.duration || 400;
	this.time = this.timeChange = 0;
	this.el = AONIC.$(el);
	this.property = property;

	this.onStart = options.onStart || function(el, opts){ 
		if(opts.end > opts.start) el.style.display = 'block'; 
	};
	this.onComplete = options.onComplete || function(el, opts){ 
		if(opts.end < opts.start) el.style.display = 'none'; 
	};
};
AONIC.api.Effects.prototype.slide = function() {
	if(this.el.style[this.property] != (this.end)+'px') this.el.style[this.property] = (this.start)+'px';
	
	setTimeout(this.onStart.bind(this, this.el, {start:this.start, end:this.end}), 10);
	this.time = new Date().getTime(); 
	this.interval = setInterval(this.setStyle.bind(this), 20);
};
AONIC.api.Effects.prototype.setStyle = function(pe) {
	var time = new Date().getTime();
	if (time < this.time + this.duration && this.el.style[this.property] != (this.end)+'px') {
		this.timeChange = time - this.time;
		this.el.style[this.property] = (this.sineInOut())+'px';
	} else {
		this.el.style[this.property] = (this.end)+'px';
		setTimeout(this.onComplete.bind(this, this.el, {start:this.start, end:this.end}), 10);
		if(this.interval) clearInterval(this.interval);
	}
};
// Transitions (c) 2003 Robert Penner (http://www.robertpenner.com/easing/), BSD License.
AONIC.api.Effects.prototype.linear = function() { return this.change*this.timeChange/this.duration + this.start; },
AONIC.api.Effects.prototype.sineInOut = function() { return -this.change/2 * (Math.cos(Math.PI*this.timeChange/this.duration) - 1) + this.start; }

/**	
 * Push Communication Framework
 * (c) 2007 - 2008 Raja Kapur <raja@aonic.net>
 *
 * Recieves push updates from servers. Uses Flash's XMLSocket object as middle layer.
 * 
 * @example
 * 	var onData = function(data) {
 * 		alert('Server said:' + data);
 * 	}
 * 	var onClose = function() {
 * 		alert('Goodbye.');
 * 	}
 * 	
 * 	var fs = new AONIC.api.PushCommunication('localhost', '3002', 'flashSock');
 * 	fs.addCallback('onData', onData).addCallback('onClose', onClose);
 * 	fs.send('My name is John. John Doe.');
 *
 * @author Raja Kapur
 * @link http://framework.aonic.net/
 */
AONIC.api.Common = function() {
	this._status = {};
	this._config = {};
};
AONIC.api.Common.prototype.setStatus = function(property, value) {
	if(property && value) {
		this._status[property] = value;
	}
};

AONIC.api.PushCommunication = function(host, port, flash) {
	if(!host || !port || !AONIC.$(flash)) {
		return;
	}
	
	this._config = {'host': host, 'port': port, 'callbacks': {'onConnect': [], 'onData': [], 'onClose': []}};
	this._flashSocket = AONIC.$(flash);
	this._status.connected = false;
	
	AONIC.instances.push(this);
	this._config.instanceId = AONIC.instances.length - 1;
	
	this._connect();
};
AONIC.api.PushCommunication.prototype = new AONIC.api.Common;

AONIC.api.PushCommunication.prototype.addCallback = function(onEvent, callback) {
	if(typeof(onEvent) == "string" && typeof(callback) == "function") {
		this._config.callbacks[onEvent].push(callback);
	}
	return this;
};
AONIC.api.PushCommunication.prototype.send = function(data) {
	if(this._flashSocket && this._flashSocket._send) {
		this._flashSocket._send(data);
	}
};
AONIC.api.PushCommunication.prototype._connect = function() {
	if(this._flashSocket && this._flashSocket._connect) {
		this._flashSocket._connect(this._config.host, this._config.port, this._config.instanceId);
	}
};
AONIC.api.PushCommunication.prototype._onConnect = function(message) {
	this._status.connected = true;
	var len = this._config.callbacks.onConnect.length;
	if(len > 0) {
		for(var i = 0; i < len; i++) {
			this._config.callbacks.onConnect[i](message);
		}
	}
};
AONIC.api.PushCommunication.prototype._onData = function(data) {
	var len = this._config.callbacks.onData.length;
	if(len > 0) {
		for(var i = 0; i < len; i++) {
			this._config.callbacks.onData[i](data);
		}
	}
};
AONIC.api.PushCommunication.prototype._onClose = function() {
	this._status.connected = true;
	var len = this._config.callbacks.onClose.length;
	if(len > 0) {
		for(var i = 0; i < len; i++) {
			this._config.callbacks.onClose[i]();
		}
	}
};
