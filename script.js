// Animations

const g9 = document.getElementById('g9');
const logo = document.getElementById('logo');
const presents = document.getElementById('presents');
const title = document.getElementById('title');
const subtitle = document.getElementById('subtitle');
const startGame = document.querySelector('#startGame');
const content = document.querySelector('.content');
const gameExplanation = document.querySelector('#gameExplanation');



document.addEventListener('DOMContentLoaded', () => {
    const elements = [g9, logo, presents, title, subtitle, startGame];
    elements.forEach(element => {
        if (element) {
            element.classList.add('hidden');
        }
    });
    runAnimations();
});
function addStartGameEventListener() {
    if (startGame) {
        startGame.addEventListener('click', hideStartScreen);
    }
}

function showElement(element) {
    if (element) {
        element.classList.remove('hidden');
        element.classList.add('fade-in');
        element.style.display = 'block';
        element.style.pointerEvents = 'auto';
    }
}

function hideElement(element) {
    if (element) {
        element.classList.remove('fade-in');
        element.classList.add('fade-out');
        setTimeout(() => {
            element.classList.add('hidden');
            element.classList.remove('fade-out');
            element.style.display = 'none';
        }, 1000);
    }
}

function finishAnimation() {
    if (title) {
        title.classList.add('final-state');
        title.style.marginTop = "20px";
    }

    showElement(subtitle);
    showElement(startGame);

    if (subtitle) {
        subtitle.style.marginTop = "10px";
        subtitle.classList.add('final-state');
    }

    if (startGame) {
        startGame.style.marginTop = "20px";
        startGame.classList.add('final-state');
    }
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
            setTimeout(() => {
                finishAnimation();
                addStartGameEventListener();
            }, 2000);
        }, 1000);
    }, 6000);
}

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
const resetButton = document.querySelector('#reset');
const distanceReset = document.querySelector('#distanceReset');



easyButton.onclick = setDifficultyEasy;
mediumButton.onclick = setDifficultyMedium;
hardButton.onclick = setDifficultyHard;
resetButton.onclick = reset;
startGame.onclick = hideStartScreen;

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

function hideStartScreen() {
    gameExplanation.style.display = "none";
    distanceReset.style.display = "block";
    menu.style.display = "block";
}
