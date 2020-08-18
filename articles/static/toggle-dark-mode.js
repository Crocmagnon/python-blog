function activateDarkMode() {
    console.log("Activating dark mode");
    document.getElementById("code-dark").removeAttribute("disabled");
}

function activateLightMode() {
    console.log("Activating light mode");
    document.getElementById("code-dark").setAttribute("disabled", "true");
}

function darkModeListener(e) {
    if (e.matches) {
        activateDarkMode();
    } else {
        activateLightMode();
    }
}

let mql = window.matchMedia("(prefers-color-scheme: dark)");
darkModeListener(mql);
mql.addListener(darkModeListener);
