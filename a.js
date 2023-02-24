const {
  wait,
  click,
  hold,
  tap,
  holdMultiple,
  sprint,
  drag,
  getCannyPixel,
} = require('.');
const robot = require('robotjs');

wait(1000);
console.log(robot.getPixelColor(710, 130));
console.log(getCannyPixel(1190, 473));
