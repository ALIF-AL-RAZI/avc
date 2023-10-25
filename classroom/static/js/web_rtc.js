

var joinButton = document.querySelector('#join_button');
var userName = '';
var mapPeers = {};
var webSocket;
function webSocketOnMessage(event) {
    debugger;
    var parseData = JSON.parse(event.data);
    var peerUserName = parseData['peer'];
    var action = parseData['action'];
    if(userName == peerUserName){
        return;
    }

    debugger;
    var receiver_channel_name = parseData['message']['receiver_channel_name'];

    if(action == 'new-peer'){
        createOfferer(peerUserName, receiver_channel_name);
        return;
    }
    if (action == 'new-offer'){
        var offer = parseData['message']['sdp'];
        createAnswerer(offer, peerUserName, receiver_channel_name);
        return;
    }

    if(action == 'new-answer'){
        var answer = parseData['message']['sdp'];
        var peer = mapPeers[peerUserName][0];
        peer.setRemoteDescription(answer);
        return;
    }
    console.log("message: ",message);
}
joinButton.addEventListener("click", function() {
    userName = joinButton.getAttribute("data-username");

    if(userName == ''){
        return;
    }

    joinButton.disabled = true;
    joinButton.style.visibility = 'hidden';

    var location = window.location;
    var wsStart = 'ws://';

    if(location.protocol == 'https:'){
        wsStart = 'wss://';
    }
    var endPoint = wsStart + location.host + '/ws'+ location.pathname;

    console.log("end Point: ", endPoint);
    debugger;
    webSocket = new WebSocket(endPoint);

    webSocket.addEventListener('open',(e)=>{
         console.log("connection open!!");
         sendSignal('new-peer', {});
    });
    webSocket.addEventListener('message', webSocketOnMessage);

    webSocket.addEventListener('closed',(e)=>{
         console.log("connection closed!!", e);
    });
    webSocket.addEventListener('error',(e)=>{
         console.log("Error occurred!!", e);
    });
});

var localStream = new MediaStream();
const constraints = {
    'video': true,
    'audio': true,
}
const localVideo = document.querySelector('#local_video');
const btnToggleAudio = document.querySelector('#btn_toggle_audio');
const btnToggleVideo = document.querySelector('#btn_toggle_video');
var userMedia = navigator.mediaDevices.getUserMedia(constraints).then(stream =>{
    localStream = stream;
    localVideo.srcObject = localStream;
    localVideo.muted = true;

    var audioTrack = stream.getAudioTracks();
    var videoTrack = stream.getVideoTracks();

    audioTrack[0].enabled = true;
    videoTrack[0].enabled = true;

    btnToggleAudio.addEventListener('click', ()=>{
        audioTrack[0].enabled = !audioTrack[0].enabled;
        if(audioTrack[0].enabled){
            btnToggleAudio.innerHTML = 'Audio Mute';
            return;
        }
        btnToggleAudio.innerHTML = 'Audio Unmute';
    });

    btnToggleVideo.addEventListener('click', ()=>{
        videoTrack[0].enabled = !videoTrack[0].enabled;
        if(videoTrack[0].enabled){
            btnToggleVideo.innerHTML = 'Video Off';
            return;
        }
        btnToggleVideo.innerHTML = 'Video On';
    });

}).catch(error=>{
    console.log("Error accessing media device", error);
});


var btnSendMsg = document.querySelector('#btn-send-msg');
var message_list = document.querySelector('#message-list');
var messageInput = document.querySelector('#msg');
btnSendMsg.addEventListener('click', sendMsgOnClick);

function getDataChannels() {
    var dataChannels = [];
    for (peerUserName in mapPeers){
        var dataChannel = mapPeers[peerUserName][1];
        dataChannels.push(dataChannel);
    }
    return dataChannels;
}

function sendMsgOnClick() {
    var message = messageInput.value;

    var li = document.createElement('li');
    li.appendChild(document.createTextNode('Me: '+ message));
    message_list.appendChild(li);
    var dataChannels = getDataChannels();
    message = userName + ': '+message;
    for(index in dataChannels){
        dataChannels[index].send(message);
    }
    messageInput.value = '';
}
function sendSignal(action, message) {
    var jsonStr = JSON.stringify({
        'peer': userName,
        'action': action,
        'message': message
    });
    webSocket.send(jsonStr);
}

function addLocalTracks(peer) {
    localStream.getTracks().forEach(track=>{
        peer.addTrack(track, localStream);
    });
    return;
}



function createVideo(peerUserName) {
    debugger;
    var videoContainer = document.querySelector('#video-container');
    var remoteVideo = document.createElement('video');
    remoteVideo.id = peerUserName + '-video';
    remoteVideo.autoplay = true;
    remoteVideo.playsInline = true;
    var videoWrapper = document.createElement('div');
    videoContainer.appendChild(videoWrapper);
    videoWrapper.appendChild(remoteVideo);
    return remoteVideo;
}

function setOnTrack(peer, remoteVideo) {
    var remoteSteam = new MediaStream();
    remoteVideo.srcObject = remoteSteam;
    peer.addEventListener('track', async (event)=>{
        remoteSteam.addTrack(event.track, remoteSteam);
    });

}

function removeVideo(remoteVideo) {
    var videoWrapper = remoteVideo.parentNode;
    videoWrapper.parentNode.removeChild(videoWrapper);

}

function createOfferer(peerUserName, receiver_channel_name) {
    debugger;
    var peer = new RTCPeerConnection(null);
    addLocalTracks(peer);
    var dc = peer.createDataChannel('channel');
    dc.addEventListener("open", ()=>{
        console.log("Connection Opened!");
    });
    dc.addEventListener('message', dcOnMessage)

    var remoteVideo = createVideo(peerUserName);
    setOnTrack(peer, remoteVideo);
    mapPeers[peerUserName] = [peer, dc];
    peer.addEventListener('iceconnectionstatechange', ()=>{
        var iceConnectionState = peer.iceConnectionState;
        if(iceConnectionState === 'failed' || iceConnectionState === 'disconnected' || iceConnectionState==='closed'){
            delete mapPeers[peerUserName];
            if(iceConnectionState!='closed'){
                peer.close();
            }
            removeVideo(remoteVideo);
        }
    });
    peer.addEventListener('icecandidate', (event)=>{
        if(event.candidate){
            console.log("new ice candidate: ", JSON.stringify(peer.localDescription));
            return;
        }
        sendSignal('new-offer', {
            'sdp':peer.localDescription,
            'receiver_channel_name': receiver_channel_name
        });
    });

    peer.createOffer()
        .then(offer => peer.setLocalDescription(offer))
        .then(() => {
            console.log('Local description set successfully.');
            return new Promise((resolve, reject) => {
                // Here, you should listen for the 'datachannel' event
                // and resolve the promise when the data channel is opened.
                peer.addEventListener('datachannel', (event) => {
                    resolve();
                });
            });
        })
        .then(() => {
            console.log('Data channel opened.');
            // Continue with other steps if needed
        })
        .catch((error) => {
            console.error('Error creating or setting descriptions:', error);
        });
}

function dcOnMessage(event) {
    var message = event.data;
    var list = document.createElement('list');
    list.appendChild(document.createTextNode(message));
    message_list.appendChild(list);
}

function createAnswerer(offer, peerUserName, receiver_channel_name) {
    debugger;
    var peer = new RTCPeerConnection(null);
    addLocalTracks(peer);

    var remoteVideo = createVideo(peerUserName);
    setOnTrack(peer, remoteVideo);

    peer.addEventListener('datachannel', e=>{
        peer.dc = e.channel;
        peer.dc.addEventListener('open', ()=>{
            console.log("connection Opened!!");
        });
        peer.dc.addEventListener('message',dcOnMessage);
        mapPeers[peerUserName] = [peer, peer.dc];
    });


    peer.addEventListener('iceconnectionstatechange', ()=>{
        var iceConnectionState = peer.iceConnectionState;
        if(iceConnectionState === 'failed' || iceConnectionState === 'disconnected' || iceConnectionState==='closed'){
            delete mapPeers[peerUserName];
            if(iceConnectionState!='closed'){
                peer.close();
            }
            removeVideo(remoteVideo);
        }
    });
    peer.addEventListener('icecandidate', (event)=>{
        if(event.candidate){
            console.log("new ice candidate: ", JSON.stringify(peer.localDescription));
            return;
        }
        sendSignal('new-answer', {
            'sdp':peer.localDescription,
            'receiver_channel_name': receiver_channel_name
        });
    });
    if (offer.type === 'offer' && (peer.signalingState === 'have-remote-offer' || peer.signalingState === 'have-local-pranswer')) {
        peer.setRemoteDescription(offer)
            .then(() => {
                console.log('Remote Description set Successfully for %s.', peerUserName);
                return peer.createAnswer();
            })
            .then((answer) => {
                console.log('Answer Created');
                return peer.setLocalDescription(answer);
            })
            .then(() => {
                console.log('Local description set for answerer.');
                sendSignal('new-answer', {
                    'sdp': peer.localDescription,
                    'receiver_channel_name': receiver_channel_name
                });
            })
            .catch((error) => {
                console.error('Error creating or setting descriptions:', error);
            });
    } else {
        console.log('Invalid offer or signaling state.');
    }
}