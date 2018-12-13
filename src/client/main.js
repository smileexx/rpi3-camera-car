// run code on load
window.addEventListener("load", function(){

    window.rc = new RCSocket();
    var game = new Game( { rc: rc } );
    game.start();
    rc.init( function () {
        game.start();
    } );


    var cam0 = document.getElementById('cam0');
    cam0.src = "http://192.168.0.52:8090/camera.mjpeg";
}, false);


/**
 * Simple class for sending/receiving messages
 *
 * @class RCSocket
 */
function RCSocket() {
    var _self = this;
    var URL = "ws://192.168.0.52:46464";
    var websocket = null;
    var isConnected = false;
    var connectionCallback = function(){};

    this.init = function ( callback ) {
        connectionCallback = callback;
        doConnect();
    };

    this.disconnect = function () {
        isConnected = false;
        websocket.close();
    };

    this.send = function (msg) {
        if(isConnected) {
            console.log("sent: ", msg);
            websocket.send(msg);
        } else {
            console.warn("Sending while not connected. MSG: ", msg);
        }
    };

    function doConnect() {
        websocket = new WebSocket(URL);
        // websocket.binaryType = 'arraybuffer';

        websocket.onopen = function (evt) {
            onOpen(evt);
        };

        websocket.onclose = function (evt) {
            onClose(evt);
        };

        websocket.onmessage = function (evt) {
            onMessage(evt);
        };

        websocket.onerror = function (evt) {
            onError(evt);
        };
    }

    function onOpen(evt) {
        isConnected = true;
        connectionCallback();
        console.log("connected");
    }

    function onClose(evt) {
        console.log( "disconnected");
    }

    function onMessage(evt) {
        console.log( "response: ", evt.data);
    }

    function onError(evt) {
        _self.disconnect();
        console.log("Error: ", evt);
    }
}


/**
 * Class for handling keys.
 * Builds as simple game loop
 *
 * @class Game
 * @param options
 */
function Game( options ) {
    'use strict';

    var _self = this;

    var gameLoopInterval = null,
        /** @type RCSocket */
        rc          = null;

    const keyUp = "ArrowUp",
        keyDown = "ArrowDown",

        keyLeft = "ArrowLeft",
        keyRight = "ArrowRight",

        keyAlt = "Alt",
        keyShift = "Shift",
        keyCtrl = "Control";

    const mask = [ "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Shift", "Control" ];

    var CONTROLS = {
        // define keys
        ArrowUp: false,
        ArrowDown: false,

        ArrowLeft: false,
        ArrowRight: false,

        Alt: false,
        Shift: false,
        Control: false
    };

    var STATE = {
        prevControls: null
    };

    if(options.rc) {
        rc = options.rc;
    }

    function gameLoop() {
        var currentControll = JSON.stringify(CONTROLS);
        if( STATE.prevControls !== currentControll ) {
            // set state
            STATE.prevControls = currentControll;

            // send sate
            // console.log(CONTROLS);
            var enc = encode(CONTROLS);
            console.log(enc);
            rc.send(enc);
        }

    }

    function keydownListener ( key ){
            switch (key) {
                case "ArrowUp":
                case "ArrowDown":
                case "ArrowLeft":
                case "ArrowRight":
                // case "Alt":
                case "Shift":
                case "Control":
                    CONTROLS[ key ] = true;
                    break;
            }
        }

    function keyupListener( key ){
            switch (key) {
                case "ArrowUp":
                case "ArrowDown":
                case "ArrowLeft":
                case "ArrowRight":
                // case "Alt":
                case "Shift":
                case "Control":
                    CONTROLS[ key ] = false;
                    break;
            }
        }

    function initKeys() {
        document.addEventListener('keydown', function (ev) {
            keydownListener(ev.key);
        });

        document.addEventListener('keyup', function (ev) {
            keyupListener(ev.key);
        });

        var classname = document.getElementsByClassName("joystick-btn");

        for (var i = 0; i < classname.length; i++) {
            classname[i].addEventListener('touchstart', function (ev) {
                keydownListener(ev.target.dataset.move);
            });
            classname[i].addEventListener('mousedown', function (ev) {
                keydownListener(ev.target.dataset.move);
            });
            classname[i].addEventListener('touchend', function (ev) {
                keyupListener(ev.target.dataset.move);
            });
            classname[i].addEventListener('mouseup', function (ev) {
                keyupListener(ev.target.dataset.move);
            });
        }
    }

    this.start = function() {
        initKeys();

        // init game loop
        _self.stop();
        gameLoopInterval = setInterval(gameLoop, 50);
    };

    this.stop = function() {
        if( gameLoopInterval ) {
            clearInterval(gameLoopInterval);
        }
    };

    /**
     * Encode pressed keys to bit mask
     */
    function encode( controls ){
        var res = '';
        mask.forEach(function(item, pos, arr) {
            res += controls[ item ] ? '1' : '0';
        });
        return parseInt(res, 2);
    }
}




