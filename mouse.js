const robot = require('robotjs');
const notifier = require('node-notifier');

const pos = robot.getMousePos();
notifier.notify({
  title: robot.getPixelColor(pos.x, pos.y),
  message: `X: ${pos.x} Y: ${pos.y}`,
  timeout: 999,
});
process.exit();
