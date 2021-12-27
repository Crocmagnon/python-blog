function copy(event) {
    const text = event.target.dataset.toCopy;
    navigator.clipboard.writeText(text).then(() => {
        console.log("Copied");
    });
}

$(document).ready(function () {
    const buttons = document.querySelectorAll(".copy-button");
    for (const button of buttons) {
        button.addEventListener("click", copy);
    }
});
