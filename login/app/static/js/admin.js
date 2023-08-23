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

  // Logout Click Event Script
  const logoutLink = document.getElementById("logout");

  if (logoutLink) {
      logoutLink.addEventListener("click", function (event) {
          event.preventDefault();

          // You can perform additional actions here before logging out

          // Redirect to the logout URL
          window.location.href = "/logout/"; // Update with your logout URL
      });
  }

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


  function toggleHiringStatus(jobPostingId) {
    fetch(`/toggle_hiring_status/${jobPostingId}/`)
        .then(response => response.json())
        .then(data => {
            // Handle success, maybe update UI or show a notification
        })
        .catch(error => {
            // Handle error, show an error message
        });
}
  
  
 

function showUpdateForm(jobId) {
  var form = document.getElementById("updateForm" + jobId);
  form.style.display = "block";
}




function closeUpdateModal(jobId) {
  var modal = document.getElementById("updateJobModal" + jobId);
  modal.style.display = "none";
}


function showUpdateModal(jobId) {
  var modal = document.getElementById("updateJobModal" + jobId);
  modal.style.display = "block";
}


function toggleHiringStatus(jobId) {
  const radioHiring = document.getElementById(`updateHiringStatusHiring_${jobId}`);
  const radioClosed = document.getElementById(`updateHiringStatusClosed_${jobId}`);
  const statusCell = document.getElementById(`statusCell_${jobId}`);
  
  if (radioHiring.checked) {
      statusCell.textContent = "Hiring";
  } else if (radioClosed.checked) {
      statusCell.textContent = "Hiring Closed";
  }
}

function updateHiringStatusInTable(jobId, newStatus) {
  var hiringStatusCell = document.getElementById("hiringStatus" + jobId);
  hiringStatusCell.innerText = newStatus;
}


function updateStatusCell(jobId) {
  const select = document.getElementById(`updateHiringStatus_${jobId}`);
  const statusCell = document.getElementById(`statusCell_${jobId}`);
  
  const selectedOption = select.options[select.selectedIndex];
  statusCell.textContent = selectedOption.textContent;
}


// inside accordio table
$(document).ready(function(){
	$('[data-toggle="tooltip"]').tooltip();
});


