const { wait, getBW, getCanny } = require('.');
const { writeFileSync } = require('fs');
const { execSync } = require('child_process');

wait(300);

const x = 1252;
const y = 375;

writeFileSync(
  'bw.json',
  JSON.stringify(getBW(x, y).map((row) => row.map((x) => +x.toFixed(3)))),
);

writeFileSync('canny.json', JSON.stringify(getCanny(x, y)));

execSync('afplay ding.mp3');
