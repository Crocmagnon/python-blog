"use strict";

function bindKey() {
    const adminLinkElement = document.querySelector("a#admin-link");
    if (adminLinkElement === undefined || adminLinkElement === null) {
        return;
    }
    const adminLocation = adminLinkElement.href;
    document.addEventListener("keydown", function (event) {
        if (event.code === "KeyE") {
            window.location = adminLocation;
        }
    });
}

((readyState) => {
    if (readyState === "interactive") {
        bindKey();
    } else if (readyState === "loading") {
        window.addEventListener("DOMContentLoaded", bindKey, false);
    }
})(document.readyState);
