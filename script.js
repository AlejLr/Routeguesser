let score = 0;
let difficulty = "medium";
let routesNum = 3;

const scoreText = document.querySelector('#scoreText');
const easyButton = document.querySelector('#easy');
const mediumButton = document.querySelector('#medium');
const hardButton = document.querySelector('#hard');
const menu = document.querySelector('#menu');
const routeNumber = document.querySelector('#routeNumber');
const resetButton = document.querySelector('#reset')

easyButton.onclick = setDifficultyEasy;
mediumButton.onclick = setDifficultyMedium;
hardButton.onclick = setDifficultyHard;
resetButton.onclick = reset;

routeNumber.addEventListener('input', updateRoutesNum);

function setDifficultyEasy() {
    difficulty = "easy";
    menu.style.display = "none";
}

function setDifficultyMedium() {
    difficulty = "medium";
    menu.style.display = "none";
}

function setDifficultyHard() {
    difficulty = "hard";
    menu.style.display = "none";
}

function reset() {
    console.log("Resetting. Work in progress")
    path = [startMarker.getLatLng()]
    polyline.setLatLngs(path);
}

function updateRoutesNum() {
    const value = parseInt(routeNumber.value);

    if (value >= 1 && value <= 10) {
        routesNum = value;
    } else {
        routesNum = 3;
    }
}