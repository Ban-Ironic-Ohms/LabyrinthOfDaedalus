import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-app.js";
import { getDatabase, ref, set, onValue } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-database.js";


const firebaseConfig = {
    databaseURL: "https://labyrinthofdaedalus-79a5f-default-rtdb.firebaseio.com/",
  };
  
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);
const db = getDatabase();

console.log("id_generator.js loaded");

document.getElementById("create_room").addEventListener("click", function() { generateID(); });

function generateID() {
    // generates a random 32 character string - letters and numbers, no special characters
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < 32; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    // checks if already used in rooms
    // result = "0000"
    const room_ref = ref(database, '/rooms/' + result + "/name");
    onValue(room_ref, (snapshot) => {
        const data = snapshot.val();
        // console.log(data);
        if ( snapshot.val() != null ) {
            console.log("ID already in use");
            generateID();
        } else {
            console.log("new room id generated: " + result);
            return result;
        }
      })

}

export { generateID };