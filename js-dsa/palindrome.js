const palindrome = (s) => {
  s = s.toLowerCase().replace(/[^a-z0-9]+/g, "")
  for (let i = 0, j = s.length - 1; i <= j; ++i, --j) {
    if (s[i] != s[j]) return false;
  }
  return true;
}

console.log(palindrome(process.argv[2]));
