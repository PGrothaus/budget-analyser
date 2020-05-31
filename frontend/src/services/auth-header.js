export default function authHeader() {
  const user = JSON.parse(localStorage.getItem('user'));
  console.log(user);
  if (user && user.access) {
    console.log("using Bearer");
    return { Authorization: 'Bearer ' + user.access };
  } else {
    console.log("NOT using Bearer");
    return {};
  }
}
