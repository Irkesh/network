<script>
// Define a function to be executed on button click
function statusUpdatek() {
    // Redirect to the 'status_update/' path
    window.location.href = "{% url 'status_update' %}"
}

// Add an event listener to the button
document.getElementById("statusUpdate").addEventListener("click", statusUpdate);
</script>