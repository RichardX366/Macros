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
