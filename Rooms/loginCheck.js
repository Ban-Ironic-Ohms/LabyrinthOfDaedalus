import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-app.js";
import { getAuth, onAuthStateChanged } from "../node_modules/firebase/firebase-auth.js";


console.log("loginCheck.js loaded");


const firebaseConfig = {
  apiKey: "AIzaSyAy70cBoQiHhkKCu2DQBiA31HOlEiSMNpY",
  authDomain: "labyrinthofdaedalus-79a5f.firebaseapp.com",
  databaseURL: "https://labyrinthofdaedalus-79a5f-default-rtdb.firebaseio.com",
  projectId: "labyrinthofdaedalus-79a5f",
  storageBucket: "labyrinthofdaedalus-79a5f.appspot.com",
  messagingSenderId: "231533789818",
  appId: "1:231533789818:web:7121ae54c94e1dd30ef1c3",
  measurementId: "G-Q1QNG1SH1Q"
};

const firebaseApp = firebase.initializeApp(firebaseConfig);

const auth = getAuth(firebaseApp);

onAuthStateChanged(auth, (user) => {
    if (user) {
        const uid = user.uid;
        console.log("User is signed in with uid: " + uid);
    } else {
        window.location.href = "auth.html";
    }
});