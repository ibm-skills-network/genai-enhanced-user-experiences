document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM content loaded');

    const wizardForm = document.getElementById('wizard-form');
    if (wizardForm) {
        wizardForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(wizardForm);
            fetch('/wizard', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(html => {
                document.body.innerHTML = html;
                // Re-attach event listeners after updating the DOM
                attachButtonListeners();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while processing your request.');
            });
        });
    }

    // Attach button listeners initially and after DOM updates
    attachButtonListeners();
});

function attachButtonListeners() {
    // Ensure all old event listeners are removed before re-attaching
    const oldDeleteButtons = document.querySelectorAll('.delete-btn');
    oldDeleteButtons.forEach(button => {
        const newElement = button.cloneNode(true);  // Clone the element to remove old listeners
        button.replaceWith(newElement);  // Replace it to ensure no previous event listeners are attached
    });

    const deleteButtons = document.querySelectorAll('.delete-btn');
    console.log('Number of delete buttons found:', deleteButtons.length);

    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopImmediatePropagation(); // Stop any other event handlers attached to this element

            if (confirm('Are you sure you want to delete this issue?')) {
                const url = this.getAttribute('data-url');
                fetch(url, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {
                    if (response.ok) {
                        this.closest('.card').remove(); // remove the issue card from the DOM
                    } else {
                        alert('Failed to delete issue');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while deleting the issue.');
                });
            }
        });
    });

    console.log('All event listeners set up');
}
