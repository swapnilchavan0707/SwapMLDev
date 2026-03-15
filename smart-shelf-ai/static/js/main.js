/**
 * Smart Shelf | Frontend Intelligence
 * Handles real-time expiry calculations and UI enhancements.
 */

document.addEventListener('DOMContentLoaded', () => {
    const itemCards = document.querySelectorAll('.item-card');

    itemCards.forEach(card => {
        // Extract data from the card's text/attributes
        const expiryDaysText = card.querySelector('.expiry-days').innerText;
        const dateAddedText = card.querySelector('.meta:nth-child(3)').innerText.split(': ')[1];

        // Parse numerical values
        const predictedLife = parseInt(expiryDaysText.match(/\d+/)[0]);
        const dateAdded = new Date(dateAddedText);
        const today = new Date();

        // Calculate days elapsed since entry
        const diffTime = Math.abs(today - dateAdded);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        const daysRemaining = predictedLife - diffDays;
        const statusBadge = card.querySelector('.status-badge');

        // Apply "Intelligence" Logic to UI
        updateVisualStatus(card, statusBadge, daysRemaining);
    });
});

/**
 * Updates the card styling based on the urgency of the expiry.
 * @param {HTMLElement} card - The item card element.
 * @param {HTMLElement} badge - The status badge element.
 * @param {number} remaining - Days left until predicted expiry.
 */
function updateVisualStatus(card, badge, remaining) {
    if (remaining <= 0) {
        badge.innerText = "Expired / Archive";
        badge.style.borderColor = "#ff4d4d";
        badge.style.color = "#ff4d4d";
        card.style.opacity = "0.6";
    } else if (remaining <= 3) {
        badge.innerText = "Priority Consumption";
        badge.style.borderColor = "#ffab00";
        badge.style.color = "#ffab00";
        // Subtle pulse effect for high priority items
        card.style.boxShadow = "0 0 15px rgba(255, 171, 0, 0.2)";
    } else {
        badge.innerText = "Fresh / Secure";
        badge.style.borderColor = "#4ade80";
        badge.style.color = "#4ade80";
    }
}

// Optional: Subtle parallax effect for the "Glassmorphism" cards
document.addEventListener('mousemove', (e) => {
    const cards = document.querySelectorAll('.glass-card');
    const xAxis = (window.innerWidth / 2 - e.pageX) / 50;
    const yAxis = (window.innerHeight / 2 - e.pageY) / 50;

    cards.forEach(card => {
        card.style.transform = `rotateY(${xAxis}deg) rotateX(${yAxis}deg)`;
    });
});