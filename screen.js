const { wait, getBW, getCanny } = require('.');
const { writeFileSync } = require('fs');
const { execSync } = require('child_process');

wait(300);

const [x, y] = [169, 645];

writeFileSync(
  'data.json',
  `${JSON.stringify(
    getBW(x, y).map((row) => row.map((x) => +x.toFixed(3))),
  )};${JSON.stringify(getCanny(x, y))};${x};${y}`,
);

execSync('afplay ding.mp3');
