// import firebase from 'https://www.gstatic.com/firebasejs/9.6.8/firebase-app.js';
// import firebaseui from 'https://www.gstatic.com/firebasejs/9.6.8/firebase-app.js';
import firebase from "../node_modules/firebase/firebase-app.js";
import firebaseui from "../node_modules/firebaseui/dist/firebaseui.js"

console.log("imported")
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
