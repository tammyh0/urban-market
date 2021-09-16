"use strict"

const createListingModal = () => {

  // Get modal
  let modal = document.querySelector('#create-listing-modal');

  // Get button that opens modal
  let btn = document.querySelector('#create-listing-btn');

  // Get modal exit button
  let close = document.querySelector('#create-listing-modal .close');

  // Get modal overlay
  let overlay = document.querySelector('.modal-overlay');

  // Opens modal when button clicked
  if (btn != null) {
    btn.addEventListener('click', (e) => {
      modal.style.display = "block";
      overlay.style.display = "block";
    });
  }

  // Close modal when button clicked
  close.addEventListener('click', (e) => {
    modal.style.display = "none";
    overlay.style.display = "none";
  });

  // When anywhere outside of modal is clicked, close it
  overlay.addEventListener('click', (e) => {
    if (e.target != modal) {
      modal.style.display = "none";
      overlay.style.display = "none";
    }
  });
}

const itemListing = () => {
  // Get Save heart icon
  // let heart = document.querySelector('.heart');

  // Get Description panel
  let description = document.querySelector('.description');

  // Get Comments panel
  let comments = document.querySelector('.comments');

  // Save/unsave with heart icon
  // if (heart != null) {
  //   heart.addEventListener('click', (e) => {
  //     if (e.target.src.includes("selected-heart-icon.png")) {
  //       e.target.src = "static/auctions/heart-icon.png";
  //     } else if (e.target.src.includes("static/auctions/heart-icon.png")) {
  //       e.target.src = "static/auctions/selected-heart-icon.png";
  //     }
  //   });
  // }

  // Open/close Description panel 
  description.addEventListener('click', (e) => {
    if (e.target.className.includes('closed')) {
      e.target.classList.remove('closed');
      e.target.classList.add('open');
      description.style.backgroundImage= "url('static/urbanmarket/minus-sign.png')";
      document.querySelector('.description-panel').style.display = "block";
    } else if (e.target.className.includes('open')) {
      e.target.classList.remove('open');
      e.target.classList.add('closed');
      description.style.backgroundImage= "url('static/urbanmarket/plus-sign.png')";
      document.querySelector('.description-panel').style.display = "none";
    }
  });

  // Open/close Comments panel 
  comments.addEventListener('click', (e) => {
    if (e.target.className.includes('closed')) {
      e.target.classList.remove('closed');
      e.target.classList.add('open');
      comments.style.backgroundImage= "url('static/urbanmarket/minus-sign.png')";
      document.querySelector('.comments-panel').style.display = "block";
      comments.style.borderBottom = "none";
      document.querySelector('.comments-panel').style.borderBottom = "1px solid #222222";
    } else if (e.target.className.includes('open')) {
      e.target.classList.remove('open');
      e.target.classList.add('closed');
      comments.style.backgroundImage= "url('static/urbanmarket/plus-sign.png')";
      document.querySelector('.comments-panel').style.display = "none";
      comments.style.borderBottom = "1px solid #222222";
    }
  });
};

const createCommentModal = () => {

  // Get modal
  let modal = document.querySelector('#create-comment-modal');

  // Get button that opens modal
  let btn = document.querySelector('#create-comment-btn');

  // Get modal exit button
  let close = document.querySelector('#create-comment-modal .close');

  // Get modal overlay
  let overlay = document.querySelector('.modal-overlay');

  // Opens modal when button clicked
  if (btn != null) {
    btn.addEventListener('click', (e) => {
      modal.style.display = "block";
      overlay.style.display = "block";
    });
  }

  // Close modal when button clicked
  close.addEventListener('click', (e) => {
    modal.style.display = "none";
    overlay.style.display = "none";
  });

  // When anywhere outside of modal is clicked, close it
  overlay.addEventListener('click', (e) => {
    if (e.target != modal) {
      modal.style.display = "none";
      overlay.style.display = "none";
    }
  });
}

createListingModal();
itemListing();
createCommentModal();