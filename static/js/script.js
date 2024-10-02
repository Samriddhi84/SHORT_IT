function ansvalidation(ev) {
    ev.preventDefault();  // Prevent the form from submitting by default

    var passValue = document.getElementById("password").value;
    var confpassValue = document.getElementById("confirm-password").value;

    // Check if the passwords match
    if (passValue !== confpassValue) {
        window.alert("Passwords do not match!");
        return false;
    } else {
        // window.alert("Passwords match! Form will be submitted.");
        // window.location.replace("/templates/main.html");
        // Submit the form

        // return true;

        return true;
    }
}
