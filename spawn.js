const { wait, click, hold, tap, holdMultiple, sprint, drag } = require('.');
const { execSync } = require('child_process');

hold('s', 200);
hold('a', 310);
sprint('w', 800);
sprint('a', 660);
sprint('w', 200);
holdMultiple(['w', 'space'], 400);
sprint('w', 3350);
holdMultiple(['a', 'space'], 400);
sprint('a', 2300);
sprint('s', 600);
sprint('a', 1250);
sprint('w', 570);
sprint('a', 4550);
sprint('w', 2750);
sprint('a', 300);
tap('e');
wait(300);
tap('e');
wait(300);
tap('e');
wait(400);
sprint('s', 2750);
sprint('d', 500);
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
tap('e');
tap('tab');
drag(470, 800, 190, 150);
click(270, 140);
tap('e');
tap('tab');
sprint('a', 1250);
sprint('s', 2000);
sprint('a', 2000);
wait(15000);
click(800, 500);
execSync('afplay ding.mp3');
