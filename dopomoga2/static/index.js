window.addEventListener('DOMContentLoaded', (event) => {
    console.log('Welcome to Dopomoga');

    document.querySelectorAll('.rjf-form-row-inner > div > label').forEach((l) => {
        l.innerHTML = gettext(l.innerHTML);
    });

    document.querySelectorAll('.rjf-add-button').forEach((b) => {
        b.innerHTML = window.TRANSLATIONS['Add item'];
    });
});
