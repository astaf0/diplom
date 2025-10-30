//отзывы
document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star-rating label');
    const radioInputs = document.querySelectorAll('.star-rating input[type="radio"]');
    let selectedRating = 0;

    stars.forEach((star, index) => {
        star.addEventListener('click', function() {
            selectedRating = index + 1;
            highlightStars(index);
        });

        star.addEventListener('mouseover', function() {
            if (selectedRating == 0) {
                highlightStars(index);
            }
        });

        star.addEventListener('mouseout', function() {
            if (selectedRating > 0) {
                highlightStars(selectedRating - 1);
            } else {
                resetStars();
            }
        });
    });

    function resetStars() {
        stars.forEach(star => {
            star.style.color = '#ddd';
        });
    }

    function highlightStars(index) {
        resetStars();
        for (let i = 0; i <= index; i++) {
            stars[i].style.color = ' #ffaa00';
        }
    }
});



//product details
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        const offset = 70;
        const elementPosition = element.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - offset;

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }
}




function changeMainImage(src) {
    const mainImg = document.querySelector('.aspect-square img');
    if (mainImg) {
        mainImg.src = src;
    }
}


