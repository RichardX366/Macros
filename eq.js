const { wait, tap } = require('.');

wait(1000);
while (true) {
  tap('e');
  wait(200);
  tap('q');
  wait(800);
}
