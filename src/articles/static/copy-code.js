"use strict";

function addCopyCode() {
    const codeBlocks = document.querySelectorAll("pre");
    codeBlocks.forEach((pre) => {
        pre.addEventListener("click", (event) => {
            if (event.detail === 4) {
                const selection = window.getSelection();
                selection.setBaseAndExtent(
                    pre.querySelector("code").firstChild,
                    0,
                    pre.querySelector("code").lastChild,
                    1,
                );
            }
        });
        pre.setAttribute("title", "Quadruple click to select all");
    });
}

((readyState) => {
    if (readyState === "interactive") {
        addCopyCode();
    } else if (readyState === "loading") {
        window.addEventListener("DOMContentLoaded", addCopyCode, false);
    }
})(document.readyState);
