// Animations


// All the constants for the anumation elements
const logo = document.getElementById('logo');
const presents = document.getElementById('presents');
const title = document.getElementById('title');
const subtitle = document.getElementById('subtitle');
const startGame = document.querySelector('#startGame');
const content = document.querySelector('.content');
const gameExplanation = document.querySelector('#gameExplanation');


// Functions for the animations

// When the page is loaded, an event listener is triggered
// The elements get hidden and the start animation begins
document.addEventListener('DOMContentLoaded', () => {
    const elements = [ logo, presents, title, subtitle, startGame];
    elements.forEach(element => {
        if (element) {
            element.classList.add('hidden');
        }
    });
    runAnimations();
});
function addStartGameEventListener() {
    // This function adds an event listener to the start game button when the button
    // is clicked the game is started and the function hideStartScreen is called

    if (startGame) {
        startGame.addEventListener('click', hideStartScreen);
    }
}

function showElement(element) {
    // This function shows the element by removing the hidden class and adding the fade-in class

    if (element) {
        element.classList.remove('hidden');
        element.classList.add('fade-in');
        element.style.display = 'block';
        element.style.pointerEvents = 'auto';
    }
}

function hideElement(element) {
    // This function hides the element by adding the hidden class and removing the fade-in class
    // As the animation shows and hides the elements, each element appears and gets hidden again

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
    // This function moves the animation to its final state, bu adjusting the title
    // and showing and positioning the subtitle and the startGame button

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

    // This function runs the animations in sequence
    // All the elements are shown and hidden one by one using a timeout
    // The final state of the animation is reached by calling the finishAnimation function

    showElement(logo);

    setTimeout(() => {
        hideElement(logo);
        setTimeout(() => {
            showElement(presents);
        }, 1000);
    }, 3000);

    setTimeout(() => {
        hideElement(presents);
        setTimeout(() => {
            showElement(title);
            setTimeout(() => {
                finishAnimation();
                addStartGameEventListener();
            }, 2000);
        }, 1000);
    }, 5000);
}


// The game logic

// Initialization of the non-constant variables in the game
let distance = 0;
let difficulty = 50;
let routesNum = 3;
let currentRound = 0;
let finalDistance = 0;
let finalOptimalDistance = 0;

let blockedRoads;
let neighbours;
let optimalDistance;
let optimalPath;
let end;
let start;

// Initialization of the constant game variables, the elements from the html
const scoreText = document.querySelector('#distanceText');
const easyButton = document.querySelector('#easy');
const mediumButton = document.querySelector('#medium');
const hardButton = document.querySelector('#hard');
const menu = document.querySelector('#menu');
const routeNumber = document.querySelector('#routeNumber');
const resetButton = document.querySelector('#reset');
const distanceReset = document.querySelector('#distanceReset');
const nextRoundButton = document.querySelector('#nextRoundButton');

const playAgainButton = document.querySelector('#playAgainButton');
const finalBarContainer = document.getElementById("finalBarContainer");

// Adding event listeners to the buttons
easyButton.onclick = setDifficultyEasy;
mediumButton.onclick = setDifficultyMedium;
hardButton.onclick = setDifficultyHard;
resetButton.onclick = resetGame;
nextRoundButton.onclick = nextRound;
playAgainButton.onclick = finishGame;
//startGame.onclick = hideStartScreen;

routeNumber.addEventListener('input', updateRoutesNum);


// Geting the information thorugh Flask

async function initializeFlask() {

    // This function fetches the data from the server by sending a POST request to the server and returns it
    // This fetch is of the type start, and gets the data for drawing the map

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

async function requestNeighbours(coords) {

    // This function works as the initialize flask function, but is of the type neighbours
    // It sends the current coordinates and gets the adjacent coordinates (neighbours)

    const send_neighbours = {"type": "neighbours", "current": coords, "difficulty": difficulty}
    try{
        const response = await fetch('http://127.0.0.1:5000/main',{
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(send_neighbours)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        neighbours = data["neighbours"];
        console.log("Requested neighbours")
        showNeighbours();
    }
    catch(error){
        console.log(error)
    }
}

// Event listener functions
function setDifficultyEasy() {

    // This function sets the difficulty to easy, hides the menu and starts the game
    // A difficulty value of 0 means there will be no blocked roads

    difficulty = 0;
    menu.style.display = "none";
    initializeGame();
}

function setDifficultyMedium() {

    // With a medium difficulty, the map will be generated with 50 blocked roads

    difficulty = 50;
    menu.style.display = "none";
    initializeGame();
}

function setDifficultyHard() {

    // Same functionality, 100 blocked roads 

    difficulty = 100;
    menu.style.display = "none";
    initializeGame();
}

function resetGame() {

    // This function resets the game by setting the distance to 0 and starting a new round
    // If the progress bar is displayed, it gets hidden, and the map gets cleared
    // In this case, startNewRound() will start the same round the player is currently playing

    console.log("Resetting")

    distance = 0;
    scoreText.innerHTML = distance;
    progressBarContainer.style.display = "none";
    clearMap();
    startNewRound();
}

function hideStartScreen() {

    // This function hides the game explanation and starts the game

    gameExplanation.style.display = "none";
    distanceReset.style.display = "block";
    menu.style.display = "block";
}

function updateRoutesNum() {

    // This function updates the number of routes the player will play
    // The value is converted to an integer and set to 3 (default) if it's out of range

    const value = parseInt(routeNumber.value);

    if (value >= 1 && value <= 10) {
        routesNum = value;
    } else {
        routesNum = 3;
    }
}

function nextRound() {

    // This function gets called when the next round button is clicked
    // It increments the current round and checks if the game is finished
    // If it is, the final score is calculated and the progress bar is shown
    // Otherwise, the progress bar is hidden and the next round starts

    barContainer.style.display = "none";
    currentRound++;
    if (currentRound === routesNum) {
        percentage = Math.round(100*(finalOptimalDistance/finalDistance));
        showBar(percentage,"final");
    }
    else{
        clearMap();
        initializeGame();
    }
}

function finishGame() {

    // This function gets called when the play again button is clicked
    // It reloads the page so the player can play again

    console.log("Game finished");
    location.reload();
}

// Helper functions (i.e. functions that are not event listeners and are called by others)

async function initializeGame(){

    // This function initializes the game by fetching the data from the server and loading it
    // It has a try statement to catch any errors that might occur due to the server not responding
    
    try{
        distance = 0;
        scoreText.innerHTML = distance;
        const data = await initializeFlask();
        console.log(data);
        console.log("Data received");
        loadData(data);
        startNewRound();
    }
    catch(error){
        console.error("Error initializing:", error);
    }
}

function loadData(data){

    // All the data gets loaded from a json dictionary (represented as an object in JS)

    blockedRoads = data["blocked nodes"];
    neighbours = data["neighbours"];
    optimalDistance = data["optimal distance"];
    optimalPath = data["optimal path"];
    end = data["end"];
    start = data["start"];
    console.log("Data loaded");
}

function updateDistance(addition) {

    // This function updates the distance by adding the length of the road traversed

    console.log(addition, typeof(addition))
    distance += parseFloat(addition);
    scoreText.innerHTML = Math.round(distance).toString();
}

function endRound() {

    // This function gets called when the end node is reached, it calculates the final and optimal distances
    // It also calculates the percentage of closeness (final score) and calls a function to show the score bar

    finalDistance += distance;
    finalOptimalDistance += optimalDistance;
    if(distance === 0){
        showBar(0, "progress");
        return;
    }

    const percentage = Math.min(100, Math.round(100*(optimalDistance/distance)));
    showBar(percentage, "progress");
}

function showBar(percentage, bar) {

    // This function shows the score of the round with a progress bar
    // The percentage is calculated and the color of the bar changes depending on the percentage

    // Variables for the elements of the progress bar
    barContainer = document.getElementById(bar+"BarContainer");
    barFill = document.getElementById(bar+"Fill");
    barText = document.getElementById(bar+"Text");

    barContainer.style.display = 'block';

    barFill.style.width = "0";
    barFill.style.backgroundColor = "red";

    setTimeout(() => {
        barFill.style.width = `${percentage}%`;

        if (percentage < 50) {
            barFill.style.backgroundColor = "red";
        } else if (percentage < 80) {
            barFill.style.backgroundColor = "yellow";
        } else {
            barFill.style.backgroundColor = "green";
        }
    }, 100);

    barText.textContent = `Score: ${percentage}%`;
}