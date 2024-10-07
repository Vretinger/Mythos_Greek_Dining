 // JavaScript to handle the delete modal
 const deleteModal = document.getElementById('deleteModal');
 deleteModal.addEventListener('show.bs.modal', function (event) {
     // Get the button that triggered the modal
     const button = event.relatedTarget; 
     // Extract the booking ID from the data-* attribute
     const bookingId = button.getAttribute('data-booking-id'); 

     // Update the form action URL
     const form = deleteModal.querySelector('#deleteBookingForm');
     form.action = `/users/delete_booking/${bookingId}/`;  // Construct the action URL directly
 });
 