'use strict';
window.onload = function () {
    const adminLinkElement = document.querySelector("a#admin-link");
    if (adminLinkElement === undefined || adminLinkElement === null) {
        return;
    }
    const adminLocation = adminLinkElement.href;
    document.addEventListener("keydown", function(event) {
        if (event.code === "KeyE") {
            window.location = adminLocation;
        }
    })
}
