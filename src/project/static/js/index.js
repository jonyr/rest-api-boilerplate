const burgerIcon = document.querySelector('#burger');
const navbarMenu = document.querySelector('#nav-links');

burgerIcon.addEventListener('click', () => {
  navbarMenu.classList.toggle('is-active');
});


// tabs
const tabs = document.querySelectorAll('.tabs li');
const tabContentBoxes = document.querySelectorAll('#tab-content > div');

tabs.forEach((tab) => {
    tab.addEventListener('click', () => {

        tabs.forEach((item) => item.classList.remove('is-active'));
        tab.classList.add('is-active');

        const target = tab.dataset.target;
        tabContentBoxes.forEach((box) => {
            if (box.getAttribute('id') === target) {
                box.classList.remove('is-hidden');
            } else {
                box.classList.add('is-hidden');
            }
        });
    });
});

// modal when sign up button is clicked
const signupButton = document.querySelector('#signup');
const modalBackground = document.querySelector('.modal-background');
const modal = document.querySelector('.modal');

signupButton.addEventListener('click', () => {
    modal.classList.add('is-active');
});

modalBackground.addEventListener('click', () => {
    modal.classList.remove('is-active');
});

