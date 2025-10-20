document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('searchForm');
    const input = document.getElementById('searchInput');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const value = input.value.trim();

        if (!value) {
            alert('Please enter an ID before searching.');
            return;
        }
        // Redirect
        window.location.href = `/submission-review/${encodeURIComponent(value)}`;
    });
});
