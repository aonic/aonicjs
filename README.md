Examples
========

## Using the Push Communication Framework

	<embed width="0" height="0" allowscriptaccess="always" name="flashSock" id="flashSock" 
	src="./swf/jsCom.swf" type="application/x-shockwave-flash"></embed>

	<script type="text/javascript">
		var onData = function(data) {
		    alert('Server said:' + data);
		}
		var onClose = function() {
		    alert('Goodbye.');
		}

		// initialize connection with server running on localhost port 3002 (included)
		var fs = new AONIC.api.PushCommunication('localhost', '3002', 'flashSock');

		fs.addCallback('onData', onData).addCallback('onClose', onClose);

		fs.send('John Doe.'); // -> alert('Server said: Welcome John Doe!');
	</script>

## Using the Effects Framework

	<div id="photoBox" style="height:0; overflow:hidden;">
		<img src="../photo.jpg" />
	</div>

	<script type="text/javascript">
		new AONIC.api.Effects('photoBox', 0, 300, 'height', {duration:300}).slide();
	</script>

## Quick and Dirty Chat Room using chatd.py and Push Framework

### Start the server: python chatd.py

### Webpage:

	<embed width="0" height="0" allowscriptaccess="always" name="flashSock" id="flashSock" 
	src="./swf/jsCom.swf" type="application/x-shockwave-flash"></embed>

	<script type="text/javascript" src="./js/AONIC.Com.js"></script>

	<script type="text/javascript">
		var fs;
		window.onload = function() {
		    // safari 3.0 needs a little more time
		    setTimeout((function() {
		        fs = new AONIC.api.PushCommunication('localhost', '3002', 'flashSock');
		    
		        fs.addLine = function(line) {
		            if(line.length == 0) return;
		            AONIC.$('chat').value += '\n'+line;
		            AONIC.$('chat').scrollTop = AONIC.$('chat').scrollHeight;
		        };
		        fs.sendMessage = function(input) {
		            var msg = input.value;
		            if(msg.length == 0) return;
		            input.value = '';
		    
		            this.send(msg);
		            if(!this.username) {
		                this.username = msg;
		                return;
		            }
		            this.addLine(this.username + '> ' + msg);
		        };
		    
		        fs.addCallback('onData', fs.addLine);
		    }), 100);
		};
	</script>

	<textarea readonly="readonly" id="chat" style="width: 600px; height: 150px; border: 0; overflow: hidden;">
	Enter a username in the input.</textarea>
	<form onsubmit="fs.sendMessage(AONIC.$('input')); return false;">
		<input type="text" id="input" style="width: 400px; font: 12px Arial;" />
	</form>
