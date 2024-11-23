// Animations
/*
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
*/
// Initiallations

let distance = 0;
let difficulty = 50;
let routesNum = 3;

let blockedNodes;
let neighbours;
let optimalDistance;
let optimalPath;
let end;
let start;

const scoreText = document.querySelector('#distanceText');
const easyButton = document.querySelector('#easy');
const mediumButton = document.querySelector('#medium');
const hardButton = document.querySelector('#hard');
const menu = document.querySelector('#menu');
const routeNumber = document.querySelector('#routeNumber');
const resetButton = document.querySelector('#reset');
const rebootButton = document.querySelector('#reboot');
const endRoundButton = document.querySelector('#endRound');
const distanceReset = document.querySelector('#distanceReset');



easyButton.onclick = setDifficultyEasy;
mediumButton.onclick = setDifficultyMedium;
hardButton.onclick = setDifficultyHard;
resetButton.onclick = resetGame;
rebootButton.onclick = startNewRound;
endRoundButton.onclick = endRound;
startGame.onclick = hideStartScreen;

routeNumber.addEventListener('input', updateRoutesNum);


// Geting the information thorugh Flask

function loadData(data){

    blockedNodes = data["blocked nodes"];
    neighbours = data["neighbours"];
    optimalDistance = data["optimal distance"];
    optimalPath = data["optimal path"];
    end = data["end"];
    start = data["start"];

    console.log("Data loaded");
    console.log("Blocked nodes:", blockedNodes);
    console.log("Neighbours:", neighbours);
    console.log("Optimal distance:", optimalDistance);
    console.log("Optimal path:", optimalPath);
    console.log("End:", end);
    console.log("Start:", start);
}

async function initializeFlask() {
    const start = {"type": "start", "difficulty": difficulty}
    try{
        const response = await fetch('http://127.0.0.1:5000/main',{
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(start)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    }
    catch(error){
        console.log(error)
    }
}

// Rest of the functions

async function startGame(){
    try{
        const data = await initializeFlask();
        console.log(data);
        console.log("Data received");
        loadData(data);
        startNewRound();
        test();
    }
    catch(error){
        console.error("Error initializing:", error);
    }
}

function setDifficultyEasy() {
    difficulty = 0;
    menu.style.display = "none";
    startGame();
}

function setDifficultyMedium() {
    difficulty = 50;
    menu.style.display = "none";
    startGame();
}

function setDifficultyHard() {
    difficulty = 100;
    menu.style.display = "none";
    startGame();
}

function resetGame() {
    console.log("Resetting. Work in progress")

    distance = 0;
    scoreText.innerHTML = distance;
    menu.style.display = "block";

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

function updateDistance(addition) {
    distance += addition;
    scoreText.innerHTML = distance;
}

function requestNeighbours(coords) {
    // do.something(idk);
    neighbours = newNeighbours // for now
    showNeighbours();
}

function endRound() {
    console.log("Round ended. Score: ", 100*distance/optimalDistance)
}