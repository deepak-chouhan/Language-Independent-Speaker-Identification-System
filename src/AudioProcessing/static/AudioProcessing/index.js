$(document).ready(() => {

    // converts the blob into base64 string
    function getString(blob, callback) {

        var batch = document.getElementById("batch").value;
        var course = document.getElementById("course").value;
        var teacher = document.getElementById("teacher").value;
        var reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = function () {
            $.post('http://127.0.0.1:8000/save', {
                "audio": JSON.stringify(reader.result),
                "batch": batch,
                "course": course,
                "teacher": teacher,
            }, function (response) {
                console.log(response)
            });
        }
    }

    var device = navigator.mediaDevices.getUserMedia({
        audio: true
    });
    var items = [];
    device.then(stream => {
        var recorder = new MediaRecorder(stream);
        recorder.ondataavailable = e => {
            items.push(e.data);

            if (recorder.state == "inactive") {
                var blob = new Blob(items, {
                    type: "audio/webm"
                });

                // display the audio on frontend
                // var audio = document.getElementById("audio");
                // var mainaudio = document.createElement("audio");
                // mainaudio.setAttribute("controls", "controls");
                // audio.appendChild(mainaudio);
                // mainaudio.innerHTML = '<source src="' + URL.createObjectURL(blob) + '" type="video/webm"/>';
                // -----------------------------
                getString(blob);
            }
        }


        const btn = document.getElementById("record")

        function record() {
            recorder.start();
            $(btn).addClass("clicked");
            setTimeout(() => {
                recorder.stop();
                $(btn).removeClass("clicked");
            }, 2000);
        }

        $(btn).click(function (e) {
            e.preventDefault();
            record();
        });
    })

})