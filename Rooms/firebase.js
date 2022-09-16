import { initializeApp } from "firebase/app";
import { getDatabase, ref, set, onValue } from "firebase/database";

console.log("something is happening")


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
const rooms_ref = ref(db, 'rooms');
onValue(rooms_ref, (snapshot) => {
  const data = snapshot.val();
  update_room(data);
});

function update_room(data) {
    document.getElementById("rooms").innerHTML = data;
}