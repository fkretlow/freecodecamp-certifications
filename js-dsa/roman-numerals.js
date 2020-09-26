const ROMAN_DIGITS = {
  1000: 'M',
  500: 'D',
  100: 'C',
  50: 'L',
  10: 'X',
  5: 'V',
  1: 'I',
};


const convert_to_roman = (number) => {
  let roman = "";
  let factor;

  for (let radix = 1000; radix >= 1 && number; radix /= 10) {
    factor = Math.floor(number / radix);
    number %= radix;

    if (radix == 1000) {
      roman += ROMAN_DIGITS[1000].repeat(factor);
    } else {
      if (factor >= 5) {
        if (factor == 9) {
          roman += ROMAN_DIGITS[radix] + ROMAN_DIGITS[radix * 10];
        } else {
          roman += ROMAN_DIGITS[radix * 5] + ROMAN_DIGITS[radix].repeat(factor - 5);
        }
      } else {
        if (factor == 4) {
          roman += ROMAN_DIGITS[radix] + ROMAN_DIGITS[radix * 5];
        } else {
          roman += ROMAN_DIGITS[radix].repeat(factor);
        }
      }
    }
  }

  return roman;
}

console.log(convert_to_roman(process.argv[2]));
