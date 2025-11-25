   // Show/hide email field based on checkbox
        const signupCheckbox = document.querySelector('input[name="signup"]');
        const emailField = document.getElementById('email-field');
        const emailInput = document.querySelector('input[name="email"]');

        if (signupCheckbox) {
            signupCheckbox.addEventListener('change', function() {
                if (this.checked) {
                    emailInput.required = true;
                    emailInput.focus();
                } else {
                    emailInput.required = false;
                    emailInput.value = '';
                }
            });

            // Show email field if checkbox is already checked (form errors)
            if (signupCheckbox.checked) {
                emailInput.required = true;
            }
        }

        // Search bar functionality
        const searchInput = document.querySelector('.search-bar input');
        const searchButton = document.querySelector('.search-bar button');

        if (searchButton) {
            searchButton.addEventListener('click', function(e) {
                e.preventDefault();
                const query = searchInput.value.trim();
                if (query) {
                    window.location.href = `/books/search/?q=${encodeURIComponent(query)}`;
                }
            });

            searchInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    searchButton.click();
                }
            });
        }
   console.log("working")
