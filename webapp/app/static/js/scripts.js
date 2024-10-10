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

function logout() {
    goTo('login.html')
}

function goTo(page) {
    window.location.href = page;
}


function backButton() {
    goTo('main.html');
}