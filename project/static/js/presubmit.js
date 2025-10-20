document.addEventListener('DOMContentLoaded', ()=> {
    const flashContainer = document.querySelector('#flash-messages .container');
    const form = document.getElementById('presubmitForm');
    const checkbox = document.getElementById('acceptCheckbox');

    // called by acceptCheck - reusable function from landing.js
    function addFlashMessage(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} mt-3`;
        alertDiv.textContent = message;
        flashContainer.appendChild(alertDiv);
    }
    // expands/collapses T's & C's
    const toggleButton = document.getElementById('toggleBtn');
    toggleButton.addEventListener('click', () => {
        const isNowCollapsed =
            document.getElementById('termsText')
            .classList.toggle('preview-collapse');
        toggleButton.classList.toggle('collapsed', isNowCollapsed);
        toggleButton.setAttribute('aria-expanded', String(!isNowCollapsed));
        document.getElementById('toggleText')
            .textContent = isNowCollapsed ? ' — Show more ▼' : ' — Show less ▲';
    });

    form.addEventListener('submit', function(event) {
        // Check validation
        if (!checkbox.checked) {
            event.preventDefault(); // stops default behaviour of submitting form
            addFlashMessage('Please check to accept the terms and conditions before submitting.', 'danger');
        }
    });
});