
// Navigation
window.onscroll = function() {
    toggleStickyHeader();
};

function toggleStickyHeader() {
    const header = document.querySelector('header');
    if (window.pageYOffset > header.offsetHeight) {
        header.classList.add('sticky');
    } else {
        header.classList.remove('sticky');
    }
}

document.querySelector('nav ul li a[href="#"]').addEventListener('click', function(event) {
    event.preventDefault();
    const confirmLogout = confirm('Are you sure you want to log out?');
    if (confirmLogout) {
        document.getElementById('logout-form').submit();
    }
});

// Home
document.querySelector('.hero button').addEventListener('click', function(e) {
    e.preventDefault();
    document.querySelector('#document-section').scrollIntoView({ behavior: 'smooth' });
});

const images = document.querySelectorAll('#document-section img');

images.forEach(image => {
    image.addEventListener('mouseenter', () => {
        image.style.transform = 'scale(1.2)';
        image.style.transition = 'transform 0.3s ease';
    });

    image.addEventListener('mouseleave', () => {
        image.style.transform = 'scale(1)';
    });
});

document.querySelector('#contact-form').addEventListener('submit', function(event) {
    let name = document.querySelector('#name').value;
    let email = document.querySelector('#email').value;
    if (name === "" || email === "") {
        event.preventDefault(); 
        alert("Please fill out all fields.");
    } else {
        alert("Your message has been sent!");
    }
});

document.getElementById("header").style.animation = "floatingBackground 5s ease-in-out infinite";

// Confirmation Dialog for Deletion
document.querySelectorAll('.btn.delete').forEach((btn) => {
    btn.addEventListener('click', (e) => {
        if (!confirm('Are you sure you want to delete this profile?')) {
            e.preventDefault();
        }
    });
});


