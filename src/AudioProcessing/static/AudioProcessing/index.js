$(document).ready(() => {

    var audioRecorder = {
        /** Stores the recorded audio as Blob objects of audio data as the recording continues*/
        audioBlobs: [],
        /*of type Blob[]*/
        /** Stores the reference of the MediaRecorder instance that handles the MediaStream when recording starts*/
        mediaRecorder: null,
        /*of type MediaRecorder*/
        /** Stores the reference to the stream currently capturing the audio*/
        streamBeingCaptured: null,
        /*of type MediaStream*/
        /** Start recording the audio
         * @returns {Promise} - returns a promise that resolves if audio recording successfully started
         */
        start: function () {
            //Feature Detection
            if (!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)) {
                //Feature is not supported in browser
                //return a custom error
                return Promise.reject(new Error('mediaDevices API or getUserMedia method is not supported in this browser.'));
            } else {
                //Feature is supported in browser

                //create an audio stream
                return navigator.mediaDevices.getUserMedia({
                        audio: true
                    } /*of type MediaStreamConstraints*/ )
                    //returns a promise that resolves to the audio stream
                    .then(stream /*of type MediaStream*/ => {

                        //save the reference of the stream to be able to stop it when necessary
                        audioRecorder.streamBeingCaptured = stream;

                        //create a media recorder instance by passing that stream into the MediaRecorder constructor
                        audioRecorder.mediaRecorder = new MediaRecorder(stream);
                        /*the MediaRecorder interface of the MediaStream Recording
                                                   API provides functionality to easily record media*/

                        //clear previously saved audio Blobs, if any
                        audioRecorder.audioBlobs = [];

                        //add a dataavailable event listener in order to store the audio data Blobs when recording
                        audioRecorder.mediaRecorder.addEventListener("dataavailable", event => {
                            //store audio Blob object
                            audioRecorder.audioBlobs.push(event.data);
                        });

                        //start the recording by calling the start method on the media recorder
                        audioRecorder.mediaRecorder.start();
                    });

                /* errors are not handled in the API because if its handled and the promise is chained, the .then after the catch will be executed*/
            }
        },
        stop: function () {
            //return a promise that would return the blob or URL of the recording
            return new Promise(resolve => {
                //save audio type to pass to set the Blob type
                let mimeType = audioRecorder.mediaRecorder.mimeType;
     
                //listen to the stop event in order to create & return a single Blob object
                audioRecorder.mediaRecorder.addEventListener("stop", () => {
                    //create a single blob object, as we might have gathered a few Blob objects that needs to be joined as one
                    let audioBlob = new Blob(audioRecorder.audioBlobs, { type: mimeType });
     
                    //resolve promise with the single audio blob representing the recorded audio
                    resolve(audioBlob);
                });
     
            //stop the recording feature
            audioRecorder.mediaRecorder.stop();
     
            //stop all the tracks on the active stream in order to stop the stream
            audioRecorder.stopStream();
     
            //reset API properties for next recording
            audioRecorder.resetRecordingProperties();
            });
        },
        stopStream: function() {
            //stopping the capturing request by stopping all the tracks on the active stream
            audioRecorder.streamBeingCaptured.getTracks() //get all tracks from the stream
                    .forEach(track /*of type MediaStreamTrack*/ => track.stop()); //stop each one
        },
        /** Reset all the recording properties including the media recorder and stream being captured*/
        resetRecordingProperties: function () {
            audioRecorder.mediaRecorder = null;
            audioRecorder.streamBeingCaptured = null;
     
            /*No need to remove event listeners attached to mediaRecorder as
            If a DOM element which is removed is reference-free (no references pointing to it), the element itself is picked
            up by the garbage collector as well as any event handlers/listeners associated with it.
            getEventListeners(audioRecorder.mediaRecorder) will return an empty array of events.*/
        }
    }

    function startAudioRecording() {
        //start recording using the audio recording API
        audioRecorder.start()
            .then(() => { //on success
                console.log("Recording Audio...")
            })
            .catch(error => { //on error
                //No Browser Support Error
                if (error.message.includes("mediaDevices API or getUserMedia method is not supported in this browser.")) {
                    console.log("To record audio, use browsers like Chrome and Firefox.");
                }
            });
    }

    function StopAudioRecording() {
        //stop the recording using the audio recording API
        console.log("Stopping Audio Recording...")
        audioRecorder.stop()
            .then(audioAsblob => { //stopping makes promise resolves to the blob file of the recorded audio
                console.log("stopped with audio Blob:", audioAsblob);
                console.log(URL.createObjectURL(audioAsblob))
     
                //Do something with the recorded audio
                //...
            })
            .catch(error => {
                //Error handling structure
                switch (error.name) {
                    case 'InvalidStateError': //error from the MediaRecorder.stop
                        console.log("An InvalidStateError has occured.");
                        break;
                    default:
                        console.log( error.message);
                };
     
            });
        }

    $("#record").click(function (e) {
        e.preventDefault();
        console.log("clicked")
        startAudioRecording()
    });

    $("#stop").click(function (e) {
        e.preventDefault();
        console.log("clicked")
        StopAudioRecording()
    });


})