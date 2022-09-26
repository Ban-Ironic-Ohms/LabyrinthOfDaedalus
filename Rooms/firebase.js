import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-app.js";
import { getDatabase, ref, set, onValue } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-database.js";


// TODO: Replace the following with your app's Firebase project configuration
// See: https://firebase.google.com/docs/web/learn-more#config-object
const firebaseConfig = {
  databaseURL: "https://labyrinthofdaedalus-79a5f-default-rtdb.firebaseio.com/",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Realtime Database and get a reference to the service
const database = getDatabase(app);

const db = getDatabase();
const rooms_ref = ref(db, '/');
onValue(rooms_ref, (snapshot) => {
  const data = snapshot.val();
  update_room(data);
});

function update_room(data) {
  console.log(data);
  // document.getElementById("rooms_lll").innerHTML += JSON.stringify(data);
  // document.getElementById("rooms_lll").innerHTML += "<br>";
}

document.querySelector("#set_room").addEventListener("click", Set, true)


function Set() {
  const main_ref = ref(database, '/');
  // firebase set function on the text inputted to the input field
  set(main_ref, document.querySelector('#input_jkl').value);
}