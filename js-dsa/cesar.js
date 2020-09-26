const rot13 = s => {
  char_codes = [];
  for (let i = 0; i < s.length; ++i) {
    char_codes.push(s.charCodeAt(i));
  }
  char_codes = char_codes.map(c => c >= 65 && c <= 90 ? (c - 65 + 13) % 26 + 65 : c);
  return String.fromCharCode(...char_codes);
};

console.log(rot13(process.argv[2]));
