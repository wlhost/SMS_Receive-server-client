$(document).ready(function() {
            if (!window.WebSocket) {
                if (window.MozWebSocket) {
                    window.WebSocket = window.MozWebSocket;
                } else {
                    console.log('Your browser doesn\'t support WebSockets.')
                }
            }
            ws = new WebSocket('ws://127.0.0.1:5000/');
            ws.onopen = function(evt) {
                console.log('Connected to chat.');

            }
            ws.onmessage = function(evt) {
                console.log(evt.data);
            }
            $('#send-message').submit(function() {
                ws.send($('#name').val() + ": " + $('#message').val());
                $('#message').val('').focus();
                return false;
            });
        });