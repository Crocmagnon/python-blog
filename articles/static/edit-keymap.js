'use strict';
// Explicitely not using ES 6 features because the compressor doesn't support them.
window.onload = function () {
    var adminLinkElement = document.querySelector("a#admin-link");
    if (adminLinkElement === undefined || adminLinkElement === null) {
        return;
    }
    var adminLocation = adminLinkElement.href;
    document.addEventListener("keydown", function(event) {
        if (event.code === "KeyE") {
            window.location = adminLocation;
        }
    })
}
