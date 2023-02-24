const {
  wait,
  click,
  hold,
  tap,
  holdMultiple,
  sprint,
  drag,
  toBrightness,
  getCannyPixel,
  closeEnough,
  exit,
  waitUntil,
} = require('.');
const robot = require('robotjs');

const overworld = [
  {
    x: 1111,
    y: 282,
    boundary: 0.3,
    movement: () => {
      hold('d', 700);
      sprint('w', 1000);
      sprint('d', 1000);
      sprint('w', 500);
      sprint('d', 1000);
      sprint('w', 500);
    },
  },
  {
    x: 919,
    y: 100,
    boundary: 0.2,
    movement: () => {
      hold('d', 800);
      sprint('w', 500);
      sprint('a', 400);
      sprint('w', 500);
      wait(500);
      hold('s', 300);
      hold('d', 700);
      sprint('w', 600);
      sprint('d', 1000);
      sprint('w', 500);
    },
  },
  {
    x: 840,
    y: 277,
    boundary: 0.4,
    movement: () => {
      hold('d', 100);
      sprint('w', 1000);
      sprint('d', 400);
      sprint('w', 800);
      sprint('d', 1000);
      sprint('w', 500);
    },
  },
  {
    x: 420,
    y: 355,
    boundary: 0.3,
    movement: () => {
      sprint('a', 350);
      sprint('w', 1000);
      sprint('a', 300);
      sprint('w', 500);
      sprint('d', 1000);
      sprint('w', 500);
    },
  },
  {
    x: 1300,
    y: 376,
    boundary: 0.2,
    movement: () => {
      hold('d', 150);
      sprint('s', 1050);
      sprint('d', 450);
      sprint('w', 400);
      wait(500);
      hold('s', 300);
      hold('d', 650);
      sprint('w', 600);
      sprint('d', 1000);
      sprint('w', 500);
    },
  },
];

const depths = [
  {
    x: 180,
    y: 270,
    boundary: 0.07,
    movement: () => {
      sprint('w', 5000);
    },
  },
  {
    x: 1220,
    y: 363,
    boundary: 0.07,
    movement: () => {
      sprint('a', 5000);
    },
  },
  {
    x: 340,
    y: 417,
    boundary: 0.1,
    movement: () => {
      sprint('w', 5000);
    },
  },
  {
    x: 1360,
    y: 481,
    boundary: 0.07,
    movement: () => {
      sprint('w', 5000);
    },
  },
  {
    x: 1200,
    y: 380,
    boundary: 0.1,
    movement: () => {
      sprint('d', 5000);
    },
  },
  {
    x: 1300,
    y: 481,
    boundary: 0.1,
    movement: () => {
      sprint('d', 5000);
    },
  },
  {
    x: 940,
    y: 111,
    boundary: 0.1,
    movement: () => {
      sprint('w', 5000);
      wait(20000);
    },
  },
];

// MUST be triggered by terminal no shortcut
wait(1000);

while (true) {
  for (let i = 0; i < 60; i++) {
    const spawn = overworld.find(
      ({ x, y, boundary }) => getCannyPixel(x, y) > boundary,
    );
    if (spawn) {
      spawn.movement();
      break;
    }
    if (i === 59) exit();
    wait(500);
  }
  hold('w', 300);
  holdMultiple(['w', 'd'], 500);
  holdMultiple(['w', 'd'], 500);
  holdMultiple(['w', 'd'], 500);
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
  for (let i = 0; i < 60; i++) {
    const room = depths.find(
      ({ x, y, boundary }) => getCannyPixel(x, y) > boundary,
    );
    if (room) {
      room.movement();
      break;
    }
    if (i === 59) exit();
    wait(500);
  }
  waitUntil(() => toBrightness(robot.getPixelColor(710, 130)) > 0.7, 60 * 3);
  wait(5000);
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
  wait(22000);
  waitUntil(() => robot.getPixelColor(920, 315) === 'dadcda');
  wait(2000);
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
