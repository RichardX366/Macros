const robot = require('robotjs');
const sleep = require('sleep');

const wait = sleep.msleep;
exports.wait = wait;

const click = (x, y) => {
  robot.moveMouse(x, y);
  wait(50);
  robot.mouseClick();
  wait(200);
};
exports.click = click;

const hold = (key, time) => {
  robot.keyToggle(key, 'down');
  wait(time);
  robot.keyToggle(key, 'up');
  wait(100);
};
exports.hold = hold;

const sprint = (key, time) => {
  robot.keyTap(key);
  wait(50);
  robot.keyToggle(key, 'down');
  wait(time);
  robot.keyToggle(key, 'up');
  wait(100);
};
exports.sprint = sprint;

const holdMultiple = (keys, time) => {
  keys.forEach((key) => robot.keyToggle(key, 'down'));
  wait(time);
  keys.forEach((key) => robot.keyToggle(key, 'up'));
  wait(100);
};
exports.holdMultiple = holdMultiple;

const tap = (key) => {
  robot.keyTap(key);
  wait(300);
};
exports.tap = tap;

const drag = (x1, y1, x2, y2) => {
  robot.moveMouse(x1, y1);
  wait(50);
  robot.mouseToggle('down');
  wait(50);
  robot.moveMouseSmooth(x2, y2, 1);
  wait(50);
  robot.mouseToggle('up');
  wait(100);
};
exports.drag = drag;
