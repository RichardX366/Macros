const { wait, click, hold, tap, sprint } = require('.');
const { execSync } = require('child_process');

wait(12000);
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
wait(6000);
execSync('afplay ding.mp3');
