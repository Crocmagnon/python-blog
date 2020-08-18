function activateDarkMode() {
    document.getElementById("code-dark").removeAttribute("disabled");
}

function activateLightMode() {
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
