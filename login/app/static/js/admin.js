
document.addEventListener('DOMContentLoaded', function () {
    // Sidebar Click Event Script
    const sidebarLinks = document.querySelectorAll('.sidebar a');
    const sections = document.querySelectorAll('.section');
  
    sidebarLinks.forEach(link => {
      link.addEventListener('click', function (event) {
        event.preventDefault();
        const targetSection = document.querySelector(link.getAttribute('href'));
        sections.forEach(section => {
          section.classList.remove('active');
        });
        targetSection.classList.add('active');
      });
    });
  
    // Modal JS
    const addJobButton = document.getElementById('addJobButton');
    const addJobModal = document.getElementById('addJobModal');
    const closeModal = document.getElementById('closeModal');
  
    addJobButton.addEventListener('click', () => {
      addJobModal.style.display = 'block';
    });
  
    closeModal.addEventListener('click', () => {
      addJobModal.style.display = 'none';
    });
  
    window.addEventListener('click', (event) => {
      if (event.target === addJobModal) {
        addJobModal.style.display = 'none';
      }
    });
  
    // Hamburger Menu
    const hamburger = document.getElementById('hamburger');
    const sidebar = document.getElementById('sidebar');
  
    hamburger.addEventListener('click', () => {
        console.log('Hamburger clicked'); // Check if this is displayed
      sidebar.classList.toggle('active');
    });
  });
  
  