/**
 * Video Speed Control Functions
 * Handles video playback speed adjustments safely
 */

// Function to double the playback speed
function doubleSpeed() {
    const video = document.querySelector('video');
    
    if (!video) {
        console.warn('No video element found');
        return;
    }
    
    // Check if playbackRate is supported
    if (typeof video.playbackRate === 'undefined') {
        console.warn('playbackRate not supported on this video element');
        return;
    }
    
    // Get current playback rate, default to 1 if undefined
    const currentRate = video.playbackRate || 1;
    
    // Double the speed, but cap at reasonable maximum (e.g., 4x)
    const newRate = Math.min(currentRate * 2, 4);
    
    // Apply the new speed
    video.playbackRate = newRate;
    
    console.log(`Playback speed changed from ${currentRate}x to ${newRate}x`);
    
    // Optional: Update UI to show current speed
    updateSpeedDisplay(newRate);
}

// Function to set specific playback speed
function setPlaybackSpeed(speed) {
    const video = document.querySelector('video');
    
    if (!video) {
        console.warn('No video element found');
        return;
    }
    
    // Validate speed input (between 0.25x and 4x)
    const validSpeed = Math.max(0.25, Math.min(4, speed));
    
    // Set the playback rate
    video.playbackRate = validSpeed;
    
    console.log(`Playback speed set to ${validSpeed}x`);
    
    // Update UI
    updateSpeedDisplay(validSpeed);
}

// Function to reset playback speed to normal (1x)
function resetSpeed() {
    const video = document.querySelector('video');
    
    if (!video) {
        console.warn('No video element found');
        return;
    }
    
    video.playbackRate = 1;
    console.log('Playback speed reset to 1x');
    
    // Update UI
    updateSpeedDisplay(1);
}

// Function to update speed display in UI
function updateSpeedDisplay(speed) {
    // Look for speed display elements
    const speedDisplay = document.querySelector('.speed-display');
    if (speedDisplay) {
        speedDisplay.textContent = `${speed.toFixed(2)}x`;
    }
    
    // Update any speed buttons or indicators
    const speedButtons = document.querySelectorAll('.speed-btn');
    speedButtons.forEach(btn => {
        btn.classList.remove('active');
        if (parseFloat(btn.dataset.speed) === speed) {
            btn.classList.add('active');
        }
    });
}

// Function to get current playback speed
function getCurrentSpeed() {
    const video = document.querySelector('video');
    
    if (!video || typeof video.playbackRate === 'undefined') {
        return 1; // Default to 1x if not available
    }
    
    return video.playbackRate || 1;
}

// Function to check if video speed controls are supported
function isSpeedControlSupported() {
    const video = document.querySelector('video');
    return video && typeof video.playbackRate !== 'undefined';
}

// Initialize speed controls when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check if speed controls are supported
    if (isSpeedControlSupported()) {
        console.log('Video speed controls are supported');
        
        // Set initial speed display
        const currentSpeed = getCurrentSpeed();
        updateSpeedDisplay(currentSpeed);
        
        // Add event listeners for speed changes
        const video = document.querySelector('video');
        video.addEventListener('ratechange', function() {
            updateSpeedDisplay(this.playbackRate);
        });
        
    } else {
        console.warn('Video speed controls are not supported');
    }
});

// Export functions for use in other modules (if using modules)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        doubleSpeed,
        setPlaybackSpeed,
        resetSpeed,
        getCurrentSpeed,
        isSpeedControlSupported
    };
}
