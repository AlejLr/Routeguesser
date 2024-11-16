// Animations
/*
const g9 = document.getElementById('g9');
const logo = document.getElementById('logo');
const presents = document.getElementById('presents');
const title = document.getElementById('title');
const subtitle = document.getElementById('subtitle');
const startGame = document.getElementById('startGame');


function showElement(element) {
    element.classList.remove('hidden');
    element.classList.add('fade-in');
}

function hideElement(element) {
    element.classList.remove('fade-in');
    element.classList.add('fade-out');
    setTimeout(() => {
        element.classList.add('hidden');
        element.classList.remove('fade-out');
    }, 1000);
}


function runAnimations() {

    showElement(g9);

    setTimeout(() => {
        hideElement(g9);
        setTimeout(() => {
            showElement(logo);
        }, 1000);
    }, 2000);

    setTimeout(() => {
        hideElement(logo);
        setTimeout(() => {
            showElement(presents);
        }, 1000);
    }, 4000);

    
    setTimeout(() => {
        hideElement(presents);
        setTimeout(() => {
            showElement(title);
        }, 1000);
    }, 6000);

    setTimeout(() => {
        hideElement(presents);
        setTimeout(() => {
            title.classList.add('change-Position');
        }, 1000);
    }, 8000);
}

document.addEventListener('DOMContentLoaded', runAnimations);
*/
// Rest of the functionality

let distance = 0;
let difficulty = "medium";
let routesNum = 3;

const scoreText = document.querySelector('#distanceText');
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
