function copy(data) {
    navigator.clipboard.writeText(data.data).then(() => {
        console.log("Copied");
    })
}

$(document).ready(function() {
    const $ = django.jQuery;
    const fileUrls = $('td.field-processed_file_url, td.field-original_file_url');
    let id = 0;
    for (let fileUrl of fileUrls) {
        fileUrl = $(fileUrl);
        const existingText = fileUrl.text().trim();
        if (!existingText) {
            continue;
        }
        const buttonId = `copy-button-${id}`;
        const copyButton = `<a class="copy-button" id="${buttonId}" href="#">&#128203;</a>`;
        let innerHTML = `<span>${existingText}</span> ${copyButton}`;
        fileUrl.html(innerHTML);
        $(`#${buttonId}`).on("click", null, existingText, copy);
        id++;
    }
});
