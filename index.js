const robot = require('robotjs');
const sleep = require('sleep');
const { execSync } = require('child_process');

const sigmoid = (x) => (1 / (1 + Math.exp(-x)) - 0.5) * 3.5;
const sigmoidLoop = (x, n) => (n === 0 ? x : sigmoidLoop(sigmoid(x), n - 1));
const toBrightness = (color) =>
  (parseInt(color.slice(0, 2), 16) +
    parseInt(color.slice(2, 4), 16) +
    parseInt(color.slice(4, 6), 16)) /
  3 /
  255;
exports.toBrightness = toBrightness;

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
  wait(500);
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

const exit = () => {
  execSync('afplay ding.mp3');
  process.exit();
};
exports.exit = exit;

const waitUntil = (func, timeout = 30) => {
  for (let i = 0; i < timeout * 2 && !func(); i++) {
    if (i === timeout * 2 - 1) exit();
    wait(500);
  }
};
exports.waitUntil = waitUntil;

const closeEnough = (color1, color2, n = 10) => {
  const r1 = parseInt(color1.slice(0, 2), 16);
  const g1 = parseInt(color1.slice(2, 4), 16);
  const b1 = parseInt(color1.slice(4, 6), 16);
  const r2 = parseInt(color2.slice(0, 2), 16);
  const g2 = parseInt(color2.slice(2, 4), 16);
  const b2 = parseInt(color2.slice(4, 6), 16);
  return (
    Math.abs(r1 - r2) < n && Math.abs(g1 - g2) < n && Math.abs(b1 - b2) < n
  );
};
exports.closeEnough = closeEnough;

const findColor = (color, x, y, width = 40, height = 40) => {
  const capture = robot.screen.capture(
    x - width / 2,
    y - height / 2,
    width,
    height,
  );

  const multiplier = capture.width / width;

  let result = false;

  new Array(height).fill(0).forEach((_, h) =>
    new Array(width).fill(0).forEach((_, w) => {
      if (closeEnough(capture.colorAt(w * multiplier, h * multiplier), color)) {
        result = true;
      }
    }),
  );

  return result;
};
exports.findColor = findColor;

const getBW = (x, y, width = 40, height = 40) => {
  const capture = robot.screen.capture(
    x - width / 2,
    y - height / 2,
    width,
    height,
  );

  const multiplier = capture.width / width;

  const bw = new Array(height).fill(0).map((_, h) =>
    new Array(width).fill(0).map((_, w) => {
      const color = capture.colorAt(w * multiplier, h * multiplier);
      return toBrightness(color);
    }),
  );

  return bw;
};
exports.getBW = getBW;

const getCanny = (x, y, width = 40, height = 40) => {
  const bw = getBW(x, y, width, height);

  const canny = bw.map((row, h) =>
    row.map((_, w) => {
      if (h === 0 || w === 0 || !bw[h + 1] || !bw[h][w + 1]) return 0;
      const x =
        bw[h - 1][w - 1] +
        bw[h][w - 1] * 2 +
        bw[h + 1][w - 1] -
        bw[h - 1][w + 1] -
        bw[h][w + 1] * 2 -
        bw[h + 1][w + 1];
      const y =
        bw[h - 1][w - 1] +
        bw[h - 1][w] * 2 +
        bw[h - 1][w + 1] -
        bw[h + 1][w - 1] -
        bw[h + 1][w] * 2 -
        bw[h + 1][w + 1];
      return +sigmoidLoop(Math.sqrt(x * x + y * y), 5).toFixed(3);
    }),
  );

  return canny;
};
exports.getCanny = getCanny;

const getCannyPixel = (x, y) => {
  const canny = getCanny(x, y, 4, 4);
  return canny[2][2];
};
exports.getCannyPixel = getCannyPixel;
