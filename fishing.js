const { wait, closeEnough, findColor, tap, exit } = require('.');
const robot = require('robotjs');

const main = () => {
  let caught = 0;
  let notFoundLoops = 1;

  while (true) {
    if (closeEnough(robot.getPixelColor(1060, 190), 'e1473f', 20)) {
      wait(100);
      notFoundLoops = 1;
      let timesClicked = 0;
      while (!findColor('fffd54', 1350, 690, 100)) {
        robot.mouseClick();
        wait(50);
        timesClicked++;
        if (timesClicked === 99) return main();
      }
      caught++;
      if (caught === 30) {
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
    notFoundLoops++;
    if (!notFoundLoops % 1000) {
      robot.mouseClick();
    }
    if (notFoundLoops === 3000) {
      exit();
    }
    wait(50);
  }
};

main();
