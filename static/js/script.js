// Interactive functionality for the website

function showMessage() {
    const messages = [
        "🎉 Awesome! You clicked the button!",
        "🐍 Python + Flask = Amazing!",
        "🚀 You're building great websites!",
        "💻 Keep coding and learning!",
        "⭐ Virtual environments rock!"
    ];
    
    const randomMessage = messages[Math.floor(Math.random() * messages.length)];
    alert(randomMessage);
}

// Add smooth scrolling for navigation links
document.addEventListener('DOMContentLoaded', function() {
    // Add click event to all navigation links
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Add a small animation effect
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });

    // Add floating animation to feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    
    featureCards.forEach((card, index) => {
        // Add staggered animation delay
        card.style.animationDelay = `${index * 0.2}s`;
        
        // Add hover effect
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Console message for developers
    console.log("🎉 Website loaded successfully!");
    console.log("💻 Built with Python Flask + HTML + CSS + JavaScript");
});