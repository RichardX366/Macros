const { getCannyPixel, wait } = require('.');

wait(1000);

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
      sprint('a', 10000);
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
    x: 573,
    y: 120,
    boundary: 0.05,
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
    x: 1190,
    y: 473,
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
      sprint('d', 1500);
      sprint('w', 9000);
    },
  },
  {
    x: 1156,
    y: 373,
    boundary: 0.1,
    movement: () => {
      sprint('a', 5000);
    },
  },
  {
    x: 60,
    y: 113,
    boundary: 0.15,
    movement: () => {
      sprint('a', 5000);
    },
  },
];

const rooms = depths.map(({ x, y, boundary }) => ({
  x,
  y,
  boundary,
  value: getCannyPixel(x, y),
}));

console.log(rooms);
