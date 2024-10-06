function login() {
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;

    if (username === "admin" && password === "1234") {
        alert("Logget inn!");
        goTo('main.html');
    } else {
        alert("Feil brukernavn eller passord.");
    }
}

function goTo(page) {
    window.location.href = page;
}
