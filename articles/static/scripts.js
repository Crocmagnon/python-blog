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

window.onload = function () {
    const adminLinkElement = document.querySelector(".article-detail .metadata a.admin-link");
    if (adminLinkElement === undefined || adminLinkElement === null) {
        return;
    }
    const adminLocation = adminLinkElement.href;
    document.addEventListener("keydown", event => {
        if (event.code === "KeyE") {
            window.location = adminLocation;
        }
    })
}
