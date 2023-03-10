const {
  wait,
  click,
  hold,
  tap,
  holdMultiple,
  sprint,
  drag,
  waitUntil,
  closeEnough,
} = require('.');
const { execSync } = require('child_process');
const robot = require('robotjs');

hold('s', 200);
hold('a', 310);
sprint('w', 1100);
sprint('a', 1600);
sprint('w', 100);
sprint('a', 1400);
sprint('s', 700);
sprint('a', 500);
sprint('s', 500);
sprint('a', 4000);
sprint('w', 1950);
sprint('a', 1700);
sprint('w', 3000);
sprint('d', 300);
sprint('w', 2550);
hold('a', 500);
tap('e');
wait(200);
tap('e');
wait(200);
tap('e');
wait(300);
sprint('d', 200);
sprint('s', 2750);
sprint('d', 300);
holdMultiple(['d', 'space'], 400);
sprint('d', 2000);
sprint('s', 2500);
sprint('a', 1000);
sprint('s', 500);
hold('space', 100);
hold('space', 100);
hold('s', 1000);
sprint('s', 1500);
sprint('a', 500);
sprint('s', 300);
sprint('d', 2600);
holdMultiple(['w', 'space'], 400);
sprint('w', 800);
sprint('d', 1500);
tap('tab');
drag(470, 800, 190, 150);
click(270, 140);
tap('tab');
sprint('a', 1500);
sprint('s', 2500);
sprint('a', 1700);
wait(12000);
waitUntil(() => closeEnough(robot.getPixelColor(920, 315), 'c5dee2'));
wait(2000);
click(800, 500);
wait(10000);
execSync('afplay ding.mp3');
