
const qrModal = document.getElementById("qrModal");
const qrBox = document.getElementById("qrBox");
const qrLink = document.getElementById("qrLink");
const copyButton = document.getElementById("copyLink");
const localNote = document.getElementById("qrLocalNote");

function getPhoneUrl() {
    const host = window.location.hostname;
    const lanIp = qrModal.dataset.lanIp;

    if ((host === "localhost" || host === "127.0.0.1") && lanIp) {
        const url = new URL(window.location.href);
        url.hostname = lanIp;
        return url.href;
    }
    return window.location.href;
}

qrModal.addEventListener("show.bs.modal", function () {
    const pageUrl = getPhoneUrl();

    qrBox.innerHTML = "";
    new QRCode(qrBox, {
        text: pageUrl,
        width: 200,
        height: 200,
        colorDark: "#0c2229",
        colorLight: "#ffffff",
    });

    qrLink.textContent = pageUrl;

    localNote.hidden = pageUrl.startsWith("https://");
});

copyButton.addEventListener("click", function () {
    const label = copyButton.querySelector("span");
    const oldText = label.textContent;

    navigator.clipboard.writeText(getPhoneUrl()).then(function () {
        label.textContent = copyButton.dataset.done;
        setTimeout(function () {
            label.textContent = oldText;
        }, 2000);
    });
});
