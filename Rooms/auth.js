import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-app.js";

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


firebase.initializeApp(firebaseConfig);

console.log("auth.js loaded");
var ui = new firebaseui.auth.AuthUI(firebase.auth());

ui.start('#firebaseui-auth-container', {
    signInOptions: [
      // List of OAuth providers supported.
      firebase.auth.GoogleAuthProvider.PROVIDER_ID
    //   firebase.auth.FacebookAuthProvider.PROVIDER_ID,
    //   firebase.auth.TwitterAuthProvider.PROVIDER_ID,
    //   firebase.auth.GithubAuthProvider.PROVIDER_ID
    ],
    // Other config options...
  });
  

var uiConfig = {
callbacks: {
    signInSuccessWithAuthResult: function(authResult, redirectUrl) {
    // User successfully signed in.
    // Return type determines whether we continue the redirect automatically
    // or whether we leave that to developer to handle.
    return true;
    },
    uiShown: function() {
    // The widget is rendered.
    // Hide the loader.
    document.getElementById('loader').style.display = 'none';
    }
},
// Will use popup for IDP Providers sign-in flow instead of the default, redirect.
signInFlow: 'popup',
signInSuccessUrl: '<url-to-redirect-to-on-success>',
signInOptions: [
    // Leave the lines as is for the providers you want to offer your users.
    firebase.auth.GoogleAuthProvider.PROVIDER_ID
//   firebase.auth.FacebookAuthProvider.PROVIDER_ID,
//   firebase.auth.TwitterAuthProvider.PROVIDER_ID,
//   firebase.auth.GithubAuthProvider.PROVIDER_ID,
//   firebase.auth.EmailAuthProvider.PROVIDER_ID,
//   firebase.auth.PhoneAuthProvider.PROVIDER_ID
],
// Terms of service url.
tosUrl: 'googel.com',
// Privacy policy url.
privacyPolicyUrl: 'google.com'
};

// The start method will wait until the DOM is loaded.
ui.start('#firebaseui-auth-container', uiConfig);
