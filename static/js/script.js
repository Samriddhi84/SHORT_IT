function ansvalidation(ev) {
    ev.preventDefault();  // Prevent the form from submitting by default

    var passValue = document.getElementById("password").value;
    var confpassValue = document.getElementById("confirm-password").value;

    // Check if the passwords match
    if (passValue !== confpassValue) {
        window.alert("Passwords do not match!");
        return false;
    } else {
        return true;
    }
}
