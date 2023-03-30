document.getElementById("calibrate-arm").onclick = function() {
    // Send an HTTP POST request to the Flask server
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:5000/calibrate-arm", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        // Update the HTML page with the detected objects
        var results = JSON.parse(xhr.responseText);
        // Do something with the results...
        print("hello");
      }
    };
    xhr.send(JSON.stringify({}));
  };