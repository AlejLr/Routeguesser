import { describe, it, beforeEach, expect, vi } from 'vitest';
import * as Script from './script.js';

const mockHTML = `
    <div id="gameExplanation">
        <div class="content">
            <img id="logo" src="logo.png" alt="Logo" class="hidden">
            <h1 id="presents" class="hidden">PRESENTS</h1>
            <h1 id="title" class="hidden">Leiden's Routeguesser</h1>
            <div id="subtitle" class="hidden"> text </div>
            <button id="startGame" class="hidden"><strong>Start Game</strong></button>
        </div>
    </div>

    <fieldset id="menu" style="display: none;">
        <legend>
            <h1>Routeguesser</h1>
        </legend>
        <div id="routeNumberDiv">
            <label for="routeNumber">Number of routes (between 1 and 10):
                <input type="number" id="routeNumber" name="routeNumber" placeholder="3 default" min=1 max=10>
            </label>
        </div>
        <div id="difficultyDiv">
            <label for="difficulty">Difficulty</label>
            <div id="difficultyButtons">
                <button class="difButton" type="button" id="easy" name="difficulty" value="0"><strong>Easy</strong></button>
                <button class="difButton" type="button" id="medium" name="difficulty" value="1"><strong>Medium</strong></button>
                <button class="difButton" type="button" id="hard" name="difficulty" value="2"><strong>Hard</strong></button>
            </div>
        </div>
    </fieldset>

    <div id="distanceReset" style="display: none;">
        <p id="distance">Distance: <strong><span id="distanceText">0</span></strong></p>
        <button id="reset">Reset</button>
    </div>

    <div id="progressBarContainer" class="hidden">
        <p id="progressText" class="barText"></p>
        <div id="progressBar" class="bar">
            <div id="progressFill" class="barFill"></div>
        </div>
        <button id="nextRoundButton" class="difButton">Next round</button>
    </div>

    <div id="finalBarContainer" style="display: none;">
        <p>Congratulations! You finished the game</p>
        <p id="finalText" class="barText"></p>
        <div id="finalBar" class="bar">
            <div id="finalFill" class="barFill"></div>
        </div>
        <button id="playAgainButton">Play again</button>
    </div>
`;

// Mock the DOM
document.body.innerHTML = mockHTML;

beforeEach(() => {
    // Reset DOM for testing independently
    document.body.innerHTML = mockHTML;

});

describe("Testing Script.js Functions", () => {
    describe("Animation-related functions", () => {
        it("should show a hidden element and set display to block", () => {
            const element1 = document.createElement('div');
            element1.classList.add('hidden');
            document.body.appendChild(element1);

            const element2 = document.createElement('div');
            element2.classList.add('hidden');
            document.body.appendChild(element2);

            Script.showElement(element1);
            Script.showElement(element2);

            expect(element1.classList.contains('hidden')).toBe(false);
            expect(element1.style.display).toBe('block');
            expect(element2.classList.contains('hidden')).toBe(false);
            expect(element2.style.display).toBe('block');
        });

        it("should hide an element", () => {
            const element1 = document.createElement('div');
            document.body.appendChild(element1);

            const element2 = document.createElement('div');
            document.body.appendChild(element2);

            Script.hideElement(element1);
            Script.hideElement(element2);

            setTimeout(() => {
                expect(element1.classList.contains('hidden')).toBe(true);
                expect(element2.classList.contains('hidden')).toBe(true);
            }, 1000);
        });
    });

    describe("Game-related functions", () => {
        it("should initialize Flask and return data", async () => {
            const mockResponse = { data: {} };
            global.fetch = vi.fn(() =>
                Promise.resolve({
                    ok: true,
                    json: () => Promise.resolve(mockResponse),
                })
            );

            const data = await Script.initializeFlask();
            expect(data).toEqual(mockResponse);
        });

        it("should request neighbours and return coordinates", async () => {
            const mockResponse = { neighbours: ["A", "B"] };
            global.fetch = vi.fn(() =>
                Promise.resolve({
                    ok: true,
                    json: () => Promise.resolve(mockResponse),
                })
            );

            await Script.requestNeighbours([0, 0]);
            expect(Script.neighbours).toEqual(mockResponse.neighbours);
        });


        it("should set difficulty and initialize the game", () => {

            Script.setDifficultyEasy();
            expect(Script.difficulty).toBe(0);

            Script.setDifficultyMedium();
            expect(Script.difficulty).toBe(50);

            Script.setDifficultyHard();
            expect(Script.difficulty).toBe(100);
        });

        it("should update the number of routes correctly", () => {
            const routeNumber = document.querySelector('#routeNumber');
            routeNumber.value = '5';
            Script.updateRoutesNum();
            expect(Script.routesNum).toBe(5);

            routeNumber.value = '15';
            Script.updateRoutesNum();
            expect(Script.routesNum).toBe(3);

            routeNumber.value = '-1';
            Script.updateRoutesNum();
            expect(Script.routesNum).toBe(3);
        });

        it("should proceed to the next round correctly", () => {
            const showBarMock = vi.spyOn(Script, "showBar");
            Script.currentRound = 0;
            Script.setRoutesNumbers(2);
            Script.nextRound();
            expect(Script.currentRound).toBe(1);
            expect(showBarMock).not.toHaveBeenCalledWith("final");

            Script.nextRound();
            expect(Script.currentRound).toBe(2);
            expect(showBarMock).toHaveBeenCalledWith("final");
        });

        it("should load data into the game state", () => {
            const mockData = {
                "blocked nodes": ["A", "B"],
                'neighbours': ["C", "D"],
                "optimal distance": 10,
                "optimal path": ["A", "D"],
                'end': [1, 1],
                'start': [0, 0],
            };

            Script.loadData(mockData);

            expect(Script.neighbours).toEqual(mockData[neighbours]);
            
        });

        it("should update the distance correctly", () => {
            Script.setDistance(0);
            Script.updateDistance(10);
            expect(Script.distance).toBe(10);
            
            Script.updateDistance(5.5);
            expect(Script.distance).toBe(15.5);
            
        });

        it("should end the round correctly", () => {
            const barContainer = document.getElementById("progressBarContainer");
            const barFill = document.getElementById("progressFill");
            const barText = document.getElementById("progressText");

            
            Script.setDistance(50);
            Script.optimalDistance = 50;
            Script.endRound();
            setTimeout(() => {
                expect(barContainer.style.display).toBe("block");
                expect(barFill.style.width).toBe("100%");
                expect(barFill.style.backgroundColor).toBe("green");
                expect(barText.textContent).toBe("Score: 100%");
            }, 150);
            
            Script.setDistance(0);
            Script.endRound();
            setTimeout(() => {
                expect(barContainer.style.display).toBe("block");
                expect(barFill.style.width).toBe("0%");
                expect(barFill.style.backgroundColor).toBe("red");
                expect(barText.textContent).toBe("Score: 0%");
            }, 150);
        });
    });

    describe("Progress bar functions", () => {
        it("should display and animate the progress bar correctly", () => {
            Script.showBar(75, "progress");

            const barContainer = document.getElementById("progressBarContainer");
            const barFill = document.getElementById("progressFill");
            const barText = document.getElementById("progressText");

            setTimeout(() => {
                expect(barContainer.style.display).toBe("block");
                expect(barFill.style.width).toBe("75%");
                expect(barFill.style.backgroundColor).toBe("yellow");
                expect(barText.textContent).toBe("Score: 75%");
            }, 150);
        });
    });
});