const telephone_check = t => {
  const re = /^(1[ -]?)?(\(\d{3}\) ?|\d{3}[ -]?)\d{3}[ -]?\d{4}$/;
  return t.match(re) ? true : false;
};

console.log(telephone_check(process.argv[2]));
