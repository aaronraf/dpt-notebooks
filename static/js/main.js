// Handle filtering notebooks by tag
document.addEventListener('DOMContentLoaded', function() {
    // We're using Alpine.js for most functionality, so this file is minimal
    
    // Handle clicking on tag chips in notebook details
    const tagChips = document.querySelectorAll('.notebook-metadata .tag');
    if (tagChips) {
        tagChips.forEach(tag => {
            tag.addEventListener('click', () => {
                // In a more complex app, this could navigate back to the index
                // with the specific tag selected
                window.location.href = 'index.html?tag=' + encodeURIComponent(tag.textContent);
            });
        });
    }
});