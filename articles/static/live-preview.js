// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.
function debounce(func, wait, immediate) {
    var timeout;
    return function () {
        var context = this, args = arguments;
        var later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

let preview = null;
window.onload = function () {
    const previewButton = document.querySelector("input#_live_preview");
    previewButton.addEventListener("click", event => {
        event.preventDefault();
        const params = "width=800,height=1000,menubar=no,toolbar=no,location=no,status=no,resizable=yes,scrollbars=yes";
        if (preview !== null) {
            preview.close();
        }
        preview = window.open("about:blank", "Preview", params);
        const id = Number(window.location.pathname.match(/\d+/)[0]);
        const loadPreview = debounce(function () {
            const body = new FormData();
            const articleContent = document.getElementById("id_content").value;
            body.set("content", articleContent);
            const csrfToken = document.querySelector("input[name=csrfmiddlewaretoken]").value;
            body.set("csrfmiddlewaretoken", csrfToken);
            fetch(`/api/render/${id}/`, {method: "POST", body: body})
                .then(function (response) {
                    response.text().then(value => {
                        preview.document.querySelector("html").innerHTML = value
                    });
                })
        }, 500);
        preview.onload = loadPreview;
        const content = document.getElementById("id_content");
        content.addEventListener("input", event => {
            event.preventDefault();
            loadPreview();
        });
    })
};
window.onbeforeunload = function () {
    if (preview !== null) {
        preview.close();
    }
};
