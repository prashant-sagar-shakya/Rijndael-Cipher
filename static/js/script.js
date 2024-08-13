document.addEventListener('DOMContentLoaded', function () {
    const encryptButton = document.querySelector('button[name="action"][value="encrypt"]');
    const decryptButton = document.querySelector('button[name="action"][value="decrypt"]');
    const textInput = document.getElementById('text');
    const keyInput = document.getElementById('key');

    function validateKeyLength() {
        const keyLength = keyInput.value.length;
        const isValid = keyLength === 16 || keyLength === 24 || keyLength === 32;
        if (!isValid) {
            keyInput.setCustomValidity('Key must be 16, 24, or 32 bytes long.');
        } else {
            keyInput.setCustomValidity('');
        }
        return isValid;
    }

    function validateInput() {
        const isTextValid = textInput.value.trim() !== '';
        const isKeyValid = validateKeyLength();
        encryptButton.disabled = !isTextValid || !isKeyValid;
        decryptButton.disabled = !isTextValid || !isKeyValid;
    }

    keyInput.addEventListener('input', validateInput);
    textInput.addEventListener('input', validateInput);

    // Initial validation
    validateInput();

    // Adding animation to form submission
    document.querySelector('form').addEventListener('submit', function () {
        document.querySelector('.container').style.transform = 'translateY(-10px)';
    });
});
