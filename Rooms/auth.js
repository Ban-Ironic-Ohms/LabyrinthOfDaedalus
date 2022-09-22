import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-app.js";
import { getAuth, onAuthStateChanged } from "../node_modules/firebase/firebase-auth.js";

var ui = new firebaseui.auth.AuthUI(firebase.auth());

ui.start('#firebaseui-auth-container', {
    signInOptions: [
      // List of OAuth providers supported.
      firebase.auth.GoogleAuthProvider.PROVIDER_ID,
    //   firebase.auth.FacebookAuthProvider.PROVIDER_ID,
    //   firebase.auth.TwitterAuthProvider.PROVIDER_ID,
    // firebase.auth.GithubAuthProvider.PROVIDER_ID
    firebase.auth.EmailAuthProvider.PROVIDER_ID
    ],
    // Other config options...
  });
  
  
  var uiConfig = {
    callbacks: {
      signInSuccessWithAuthResult: function(authResult, redirectUrl) {
        // User successfully signed in.
    // Return type determines whether we continue the redirect automatically
    // or whether we leave that to developer to handle.
    return false;
  },
  uiShown: function() {
    // The widget is rendered.
    // Hide the loader.
    document.getElementById('loader').style.display = 'none';
  }
},
// Will use popup for IDP Providers sign-in flow instead of the default, redirect.
signInFlow: 'popup',
signInSuccessUrl: 'auth.html',
signInOptions: [
  firebase.auth.GoogleAuthProvider.PROVIDER_ID,
  firebase.auth.EmailAuthProvider.PROVIDER_ID,
],

// Terms of service url.
tosUrl: 'google.com',
// Privacy policy url.
privacyPolicyUrl: 'google.com'
};

// The start method will wait until the DOM is loaded.
ui.start('#firebaseui-auth-container', uiConfig);

function printUserInfo(user=auth.user) {
  if (user) {
    // User is signed in, see docs for a list of available properties
    // https://firebase.google.com/docs/reference/js/firebase.User
    const uid = user.uid;
    const email = user.email;
    const emailVerified = user.emailVerified;
    const displayName = user.displayName;
    // const photoURL = user.photoURL;
    // const phoneNumber = user.phoneNumber;
    // const isAnonymous = user.isAnonymous;
    // const tenantId = user.tenantId;
    // const providerData = user.providerData;
    const token = user.getIdToken();
    console.log("uid" + uid);
    console.log("email" + email);
    console.log("emailVerified" + emailVerified);
    console.log("displayName" + displayName);
    console.log("token" + token);
  }
}

console.log("auth.js loaded");
const auth = getAuth();
console.log(auth)

function getUserInfo() {
  const user = auth.currentUser;

  if (user) {
    console.log("this runs")
  }
}
getUserInfo()

onAuthStateChanged(auth, (user) => {
  if (user) {
    // User is signed in, see docs for a list of available properties
    // https://firebase.google.com/docs/reference/js/firebase.User
    const uid = user.uid;
    const email = user.email;
    const emailVerified = user.emailVerified;
    const displayName = user.displayName;
    // const photoURL = user.photoURL;
    // const phoneNumber = user.phoneNumber;
    // const isAnonymous = user.isAnonymous;
    // const tenantId = user.tenantId;
    // const providerData = user.providerData;
    const token = user.getIdToken();
    console.log("uid" + uid);
    console.log("email" + email);
    console.log("emailVerified" + emailVerified);
    console.log("displayName" + displayName);
    console.log("token" + token);

  } else {
    console.log("DEATH TO USERS")
  }
});