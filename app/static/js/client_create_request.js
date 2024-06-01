


document.addEventListener("DOMContentLoaded", () => {
    const servicesSelect = document.getElementById("service_id");
    const serviceCostInput = document.getElementById("serviceCost");
    servicesSelect.addEventListener("change", function() {
        serviceCostInput.value = parseFloat(servicesSelect.options[servicesSelect.selectedIndex].getAttribute("cost"));
    })

    servicesSelect.dispatchEvent(new Event("change"));
})