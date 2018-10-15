// run code on load
window.addEventListener("load", function(){

    var rc = new RCSocket();
    var game = new Game( { rc: rc } );
    game.start();
    rc.init( function () {
        game.start();
    } );

}, false);


/**
 * Simple class for sending/receiving messages
 *
 * @class RCSocket
 */
function RCSocket() {
    var _self = this;
    var URL = "ws://127.0.0.1:8000/";
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
            rc.send(currentControll);
        }

    }

    function initKeys() {
        document.addEventListener('keydown', function( e ){
            switch (e.key) {
                case "ArrowUp":
                case "ArrowDown":
                case "ArrowLeft":
                case "ArrowRight":
                case "Alt":
                case "Shift":
                case "Control":
                    CONTROLS[ e.key ] = true;
                    break;
            }
        });

        document.addEventListener('keyup', function( e ){
            switch (e.key) {
                case "ArrowUp":
                case "ArrowDown":
                case "ArrowLeft":
                case "ArrowRight":
                case "Alt":
                case "Shift":
                case "Control":
                    CONTROLS[ e.key ] = false;
                    break;
            }
        });

    }

    this.start = function() {
        initKeys();

        // init game loop
        _self.stop();
        gameLoopInterval = setInterval(gameLoop, 200);
    };

    this.stop = function() {
        if( gameLoopInterval ) {
            clearInterval(gameLoopInterval);
        }
    };
}




