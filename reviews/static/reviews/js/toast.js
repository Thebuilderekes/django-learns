    // 3. JavaScript to Make the Toast Disappear
    document.addEventListener('DOMContentLoaded', function() {
        const toast = document.getElementById('toast-message');
        
        if (toast) {
            // Get the time defined by the CSS animation (3 seconds)
            const animationDurationMs = 3000; 

            // Wait for the animation duration (plus a little buffer)
            setTimeout(function() {
                // Apply the 'fade-out' class to start the opacity transition
                toast.classList.add('fade-out');
            }, animationDurationMs);

            // Wait a little longer (e.g., 500ms) for the fade-out to finish
            // before removing it completely from the DOM.
            setTimeout(function() {
                toast.remove();
            }, animationDurationMs + 500); 
        }
    });
