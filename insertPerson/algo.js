var es = [0.5, 0.55, 0.66, 0.65, 0.45, 0.5];
var ts = [0, 1, 2, 3, 4, 5, 6];

/*
Data is currently just a list of floats, this function will calculate
the global max and min and also the integral can be used to calculate
the shape of the curve.

No return so that y'all can figure out what you need.
*/
function place_icon(data) {
  average = (data[data.length - 1] + data[0]) / data.length;

  integral = 0;

  for (i = 0; i < data.length; i++) {
    integral += data[i] - average;
  }
  maxIndex = 0;
  minIndex = 0;
  for (i = 1; i < data.length - 1; i++) {
    if (
      data[i] > data[i + 1] &&
      data[i] > data[i - 1] &&
      data[i] >= data[maxIndex]
    ) {
      maxIndex = i;
    }
    if (
      data[i] < data[i + 1] &&
      data[i] < data[i - 1] &&
      data[i] <= data[minIndex]
    ) {
      minIndex = i;
    }
    if (data[i] < data[data.length - 1]) {
      maxIndex = data.length - 1;
    }
    if (data[i] > data[data.length - 1]) {
      minIndex = data.length - 1;
    }
  }
}
