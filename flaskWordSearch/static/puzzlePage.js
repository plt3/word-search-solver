const MIN_DIM = Math.min.apply(null, [window.innerHeight, window.innerWidth]) * .97;
const PUZZLE_TABLE = document.getElementsByTagName('table')[0];

PUZZLE_TABLE.style.width = MIN_DIM + 'px';
PUZZLE_TABLE.style.height = MIN_DIM + 'px';

// TODO: write some magical function to parse disgusting, shameful, gross ersatz JSON
// in each word's ID and then find corresponding starting letter and highlight the word
// Also figure out how to make words list fit on the page next to the grid depending on
// if it's on mobile or not
