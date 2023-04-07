const { wait, closeEnough, findColor } = require('.');
const robot = require('robotjs');

const main = () => {
  let caught = 0;
  let notFountLoops = 0;

  while (true) {
    if (closeEnough(robot.getPixelColor(1250, 200), 'e1473f', 20)) {
      wait(100);
      notFountLoops = 0;
      let timesClicked = 0;
      while (!findColor('fffd54', 1590, 810, 100)) {
        robot.mouseClick();
        wait(50);
        timesClicked++;
        if (timesClicked === 99) return main();
      }
      caught++;
      if (caught === 10) {
        caught = 0;
        tap('0');
        wait(200);
        robot.mouseClick();
        wait(1000);
        tap('8');
      }
      wait(500);
      robot.mouseClick();
    }
    notFountLoops++;
    if (notFountLoops === 1000) {
      notFountLoops = 0;
      robot.mouseClick();
    }
    wait(50);
  }
};

main();
