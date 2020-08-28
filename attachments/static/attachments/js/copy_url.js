function copy(data) {
    navigator.clipboard.writeText(data).then(() => {
        console.log("Copied");
    })
}

$(document).ready(function() {
    const $ = django.jQuery;
    const fileUrls = $('td.field-processed_file_url, td.field-original_file_url');
    for (let fileUrl of fileUrls) {
        fileUrl = $(fileUrl);
        const existingText = fileUrl.text().trim();
        if (!existingText) {
            continue;
        }
        const copyButton = `<a class='copy-button' href='#' onclick="copy(\'${existingText}\')">&#128203;</a>`;
        let innerHTML = `<span>${existingText}</span> ${copyButton}`;
        fileUrl.html(innerHTML);
    }
});
