window.onload = function () {
    const previewButton = document.querySelector("input#_live_preview");
    previewButton.addEventListener("click", openPreviewPopup);
};
window.onbeforeunload = function () {
    if (preview !== null) {
        preview.close();
    }
};

let preview = null;

function openPreviewPopup(event) {
    event.preventDefault();
    const params = "width=800,height=1000,menubar=no,toolbar=no,location=no,status=no,resizable=yes,scrollbars=yes";
    if (preview !== null) {
        preview.close();
    }
    preview = window.open("about:blank", "Preview", params);

    setTimeout(loadPreview, 1000);
    setupLivePreview();
}

function loadPreview() {
    const id = Number(window.location.pathname.match(/\d+/)[0]);
    const body = new FormData();
    const articleContent = document.getElementById("id_content").value;
    body.set("content", articleContent);
    const csrfToken = document.querySelector("input[name=csrfmiddlewaretoken]").value;
    body.set("csrfmiddlewaretoken", csrfToken);
    fetch(`/api/render/${id}/`, {method: "POST", body: body})
        .then(function (response) {
            response.text().then(value => {
                preview.document.open("text/html", "replace");
                preview.document.write(value);
                preview.document.close();
            });
        })
}

function setupLivePreview() {
    const debouncedLoadPreview = debounce(loadPreview, 500);
    const content = document.getElementById("id_content");
    content.addEventListener("input", event => {
        event.preventDefault();
        debouncedLoadPreview();
    });
}

/**
 * Returns a function, that, as long as it continues to be invoked, will not
 * be triggered. The function will be called after it stops being called for
 * `wait` milliseconds.
 */
function debounce(func, wait) {
    let timeout;
    return function () {
        const context = this, args = arguments;
        const later = function () {
            timeout = null;
            func.apply(context, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
