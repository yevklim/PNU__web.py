for (const el of document.querySelectorAll(".fix-offset-top")) {
    el.style.setProperty("top", `${el.offsetTop}px`);
}
