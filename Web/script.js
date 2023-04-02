const calibrateBtn = document.getElementById('calibrate-arm');

calibrateBtn.addEventListener('click', () => {
  fetch('http://127.0.0.1:5000/calibrate1') 
    .then(response => {
      console.log(response);
    })
    .catch(error => {
      console.error(error);
    });
});