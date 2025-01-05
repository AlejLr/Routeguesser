import { describe, it, beforeEach, expect, vi } from 'vitest';
import { mockHTML } from './mockHtml.js';
import * as Script from './script.js';

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

        it("should display title, subtitle, and startGame", () => {
            const title = document.getElementById('title');
            const subtitle = document.getElementById('subtitle');
            const startGame = document.getElementById('startGame');

            Script.finishAnimation();

            expect(title.classList.contains('final-state')).toBe(true);
            expect(subtitle.classList.contains('final-state')).toBe(true);
            expect(startGame.classList.contains('final-state')).toBe(true);
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

        it("should set difficulty and call initializeGame", () => {
            const initializeGameMock = vi.spyOn(Script, "initializeGame");

            Script.setDifficultyEasy();
            expect(Script.difficulty).toBe(0);
            expect(document.getElementById("menu").style.display).toBe("none");
            expect(initializeGameMock).toHaveBeenCalled();

            Script.setDifficultyMedium();
            expect(Script.difficulty).toBe(50);
            expect(document.getElementById("menu").style.display).toBe("none");
            expect(initializeGameMock).toHaveBeenCalled();

            Script.setDifficultyHard();
            expect(Script.difficulty).toBe(100);
            expect(document.getElementById("menu").style.display).toBe("none");
            expect(initializeGameMock).toHaveBeenCalled();
        });

        it("should reset the game correctly", () => {
            const scoreText = document.getElementById("distanceText");
            const progressBarContainer = document.getElementById("progressBarContainer");
            Script.resetGame();
            expect(Script.distance).toBe(0);
            expect(scoreText.innerHTML).toBe("0");
            expect(progressBarContainer.style.display).toBe("none");
        });

        it("should hide the start screen and show the menu", () => {
            const gameExplanation = document.getElementById("gameExplanation");
            const distanceReset = document.getElementById("distanceReset");
            const menu = document.getElementById("menu");
            Script.hideStartScreen();
            expect(gameExplanation.style.display).toBe("none");
            expect(distanceReset.style.display).toBe("block");
            expect(menu.style.display).toBe("block");
        });

        it("should update the number of routes correctly", () => {
            const input = document.getElementById("routeNumber");
            input.value = "5";
            Script.updateRoutesNum();
            expect(Script.routesNum).toBe(5);

            input.value = "15";
            Script.updateRoutesNum();
            expect(Script.routesNum).toBe(3); // Default value

            input.value = "-1";
            Script.updateRoutesNum();
            expect(Script.routesNum).toBe(3); // Default value
        });

        it("should proceed to the next round correctly", () => {
            const showBarMock = vi.spyOn(Script, "showBar");
            Script.currentRound = 0;
            Script.routesNum = 2;
            Script.nextRound();
            expect(Script.currentRound).toBe(1);
            expect(showBarMock).not.toHaveBeenCalledWith("final");

            Script.nextRound();
            expect(Script.currentRound).toBe(2);
            expect(showBarMock).toHaveBeenCalledWith("final");
        });

        it("should finish the game and reload the page", () => {
            const reloadMock = vi.fn();
            Object.defineProperty(window.location, 'reload', {
                configurable: true,
                value: reloadMock,
            });
            Script.finishGame();
            expect(reloadMock).toHaveBeenCalled();
        });

        it("should initialize the game correctly", async () => {
            const initializeFlaskMock = vi.spyOn(Script, "initializeFlask").mockResolvedValue({ data: {} });
            const loadDataMock = vi.spyOn(Script, "loadData").mockImplementation(() => {});

            await Script.initializeGame();

            expect(Script.distance).toBe(0);
            expect(initializeFlaskMock).toHaveBeenCalled();
            expect(loadDataMock).toHaveBeenCalled();
        });

        it("should load data into the game state", () => {
            const mockData = {
                "blocked nodes": ["A", "B"],
                neighbours: ["C", "D"],
                "optimal distance": 10,
                "optimal path": ["A", "D"],
                end: [1, 1],
                start: [0, 0],
            };

            Script.loadData(mockData);

            expect(Script.blockedRoads).toEqual(mockData["blocked nodes"]);
            expect(Script.neighbours).toEqual(mockData["neighbours"]);
            expect(Script.optimalDistance).toEqual(mockData["optimal distance"]);
        });

        it("should update the distance correctly", () => {
            Script.distance = 0;
            Script.updateDistance(10);
            expect(Script.distance).toBe(10);
            expect(document.getElementById("distanceText").innerHTML).toBe("10");

            Script.updateDistance(5.5);
            expect(Script.distance).toBe(15.5);
            expect(document.getElementById("distanceText").innerHTML).toBe("16");
        });

        it("should end the round correctly", () => {
            const showBarMock = vi.spyOn(Script, "showBar");
            Script.distance = 100;
            Script.optimalDistance = 50;
            Script.endRound();
            expect(showBarMock).toHaveBeenCalledWith(50, "progress");

            Script.distance = 0;
            Script.endRound();
            expect(showBarMock).toHaveBeenCalledWith(0, "progress");
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