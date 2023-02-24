const {
  wait,
  click,
  hold,
  tap,
  holdMultiple,
  sprint,
  drag,
  toBrightness,
} = require('.');
const robot = require('robotjs');

const overworld = [{ x: 470, y: 800, boundary: 0.1, movement: () => {} }];

const depths = [{ x: 470, y: 800, boundary: 0.1, movement: () => {} }];

// MUST be triggered by terminal no shortcut
wait(1000);

while (true) {
  // Move to spawn spot
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
  sprint('w', 2500);
  hold('a', 300);
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
  sprint('w', 900);
  sprint('d', 1500);
  tap('tab');
  drag(470, 800, 190, 150);
  click(270, 140);
  tap('tab');
  sprint('a', 1300);
  sprint('s', 2500);
  sprint('a', 1700);
  while (robot.getPixelColor(912, 438) !== 'c6dee2') wait(500);
  wait(2000);
  click(800, 500);
  wait(10000);
  // Kill self in depths
  while (toBrightness(robot.getPixelColor(840, 140)) < 0.7) {
    wait(500);
  }
  sprint('a', 400);
  sprint('s', 2000);
  sprint('d', 400);
  sprint('s', 4000);
  sprint('d', 300);
  sprint('s', 1700);
  sprint('a', 400);
  sprint('s', 1800);
  tap('e');
  tap('e');
  tap('1');
  tap('1');
  tap('1');
  tap('1');
  tap('1');
  tap('1');
  tap('1');
  tap('1');
  tap('e');
  tap('e');
  tap('1');
  tap('1');
  wait(26000);
  click(800, 500);
  wait(2000);
  click(110, 333);
  click(1111, 320);
  click(120, 370);
  click(595, 220);
  click(850, 560);
  click(540, 265);
  click(850, 560);
  click(540, 285);
  click(850, 560);
  click(540, 305);
  click(850, 560);
  click(540, 325);
  click(850, 560);
  click(540, 345);
  click(850, 560);
  click(540, 365);
  click(850, 560);
  click(540, 385);
  click(850, 560);
  click(540, 405);
  click(850, 560);
  click(540, 425);
  click(850, 560);
  click(720, 745);
  wait(10000);
}
