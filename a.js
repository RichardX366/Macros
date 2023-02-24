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
console.log(getCannyPixel(1200, 380));
