const { wait, click, hold, tap, holdMultiple, sprint, drag } = require('.');
const robot = require('robotjs');

wait(1000);
console.log(robot.getPixelColor(912, 438));
