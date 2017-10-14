var song_option_1 = 0;
var song_option_2 = 0;
var song_option_3 = 0;
var song_option_4 = 0;
var song_option_5 = 0;

function refreshResults () {
  var results = document.getElementById('results');
  results.innerHTML += '<br />song_option_1: ' + song_option_1;
  results.innerHTML += '<br />song_option_2: ' + song_option_2;
  results.innerHTML += '<br />song_option_3: ' + song_option_3;
  results.innerHTML += '<br />song_option_4: ' + song_option_4;
  results.innerHTML += '<br />song_option_5: ' + song_option_5;
}

document.getElementById('song_option_1-button').addEventListener('click', function () {
  song_option_1++;
  refreshResults();
});

document.getElementById('song_option_2-button').addEventListener('click', function () {
  song_option_2++;
  refreshResults();
});

document.getElementById('song_option_3-button').addEventListener('click', function () {
  song_option_3++;
  refreshResults();
});

document.getElementById('song_option_4-button').addEventListener('click', function () {
  song_option_4++;
  refreshResults();
});

document.getElementById('song_option_5-button').addEventListener('click', function () {
  song_option_5++;
  refreshResults();
});