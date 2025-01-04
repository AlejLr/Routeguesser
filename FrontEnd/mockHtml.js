// This is a mock html constant that will be injected into the DOM for the test

export const mockHTML = `
<div id="gameExplanation">
    <div class="content">
        <img id="logo" src="logo.png" alt="Logo" class="hidden">
        <h1 id="presents" class="hidden">PRESENTS</h1>
        <h1 id="title" class="hidden">Leiden's Routeguesser</h1>
        <p id="subtitle" class="hidden">explanation and rules</p>
        <button id="startGame" class="hidden"><strong>Start Game</strong></button>
    </div>
</div>

<fieldset id="menu">
    <legend>
        <h1>Routeguesser</h1>
    </legend>

    <div id="routeNumberDiv">
        <label for="routeNumber">Number of routes (between 1 and 10):
            <input type="number" id="routeNumber" name="routeNumber" placeholder="3 default"
                min=1 max=10>
        </label>
    </div>
    <div id="difficultyDiv">
        <label for="difficulty">Difficulty</label>
        <div id="difficultyButtons">
            <button class ="difButton" type="button" id="easy" name="difficulty" value="0"><strong>Easy</strong></button>
            <button class ="difButton" type="button" id="medium" name="difficulty" value="1"><strong>Medium</strong></button>
            <button class ="difButton" type="button" id="hard" name="difficulty" value="2"><strong>Hard</strong></button>
        </div>
    </div>
</fieldset>

<div id="map"></div>

<div id="distanceReset">
    <p id="distance">Distance: <strong><span id = "distanceText">0</span></strong></p>
    <button id="reset">Reset</button>
</div>

<div id="progressBarContainer" class="hidden">
    <p id="progressText" class="barText"></p>
    <div id="progressBar" class="bar">
        <div id="progressFill" class="barFill"></div>
    </div>
    <button id="nextRoundButton" class="difButton">Next round</button>
</div>

<div id="finalBarContainer">
    <p>Congratulations! You finished the game</p>
    <p id="finalText" class="barText"></p>
    <div id="finalBar" class="bar">
        <div id="finalFill" class="barFill"></div>
    </div>
    <button id="playAgainButton">Play again</button>
</div>
`;