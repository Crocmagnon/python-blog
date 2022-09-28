let preview = null;

function onLoad() {
    const previewButton = document.querySelector("input#_live_preview");
    if (previewButton) {
        previewButton.addEventListener("click", openPreviewPopup);
    }
}
((readyState) => {
    if (readyState === "interactive") {
        onLoad();
    } else if (readyState === "loading") {
        window.addEventListener("DOMContentLoaded", onLoad, false);
    }
})(document.readyState);

window.onbeforeunload = function () {
    if (preview !== null) {
        preview.close();
    }
};

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
    const body = prepareBody();
    const scrollX = preview.scrollX || 0;
    const scrollY = preview.scrollY || 0;
    fetch(`/api/render/${id}/`, { method: "POST", body: body })
        .then((response) => {
            return response.text();
        })
        .then((value) => {
            preview.document.open("text/html", "replace");
            preview.document.write(value);
            preview.document.close();
            preview.scrollTo(scrollX, scrollY);
        })
        .catch(console.error);
}

function prepareBody() {
    const body = new FormData();
    const inputs = [
        {
            selector: "#id_content",
            property: "value",
            to: "content",
        },
        {
            selector: "input[name=csrfmiddlewaretoken]",
            property: "value",
            to: "csrfmiddlewaretoken",
        },
        {
            selector: "#id_has_code",
            property: "checked",
            to: "has_code",
        },
        {
            selector: "#id_title",
            property: "value",
            to: "title",
        },
        {
            selector: "#id_custom_css",
            property: "value",
            to: "custom_css",
        },
    ];
    for (const input of inputs) {
        const element = document.querySelector(input.selector);
        body.set(input.to, element[input.property]);
    }
    const tagIds = Array.from(document.querySelector("#id_tags").selectedOptions)
        .map((option) => option.value)
        .join();
    body.set("tag_ids", tagIds);

    return body;
}

function setupLivePreview() {
    const debouncedLoadPreview = debounce(loadPreview, 200);

    function listener(event) {
        event.preventDefault();
        debouncedLoadPreview();
    }
    const ids = ["id_content", "id_title", "id_has_code", "id_custom_css"];
    for (const id of ids) {
        const element = document.getElementById(id);
        element.addEventListener("input", listener);
    }
}

/**
 * Returns a function, that, as long as it continues to be invoked, will not
 * be triggered. The function will be called after it stops being called for
 * `wait` milliseconds.
 */
function debounce(func, wait) {
    let timeout;

    return function () {
        const context = this,
            args = arguments;
        const later = function () {
            timeout = null;
            func.apply(context, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
