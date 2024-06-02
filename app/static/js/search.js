document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("searchInput");
    const table = document.getElementsByTagName("table")[0];
    const tbody = table.getElementsByTagName("tbody")[0];
    const rows = tbody.getElementsByTagName("tr");
    const searchColumnIndex = 1; // Задайте индекс колонки для поиска (начиная с 0)

    searchInput.addEventListener("keyup", function() {
        const filter = searchInput.value.toLowerCase();

        for (let row of rows) {
            const cell = row.getElementsByTagName("td")[searchColumnIndex];
            if (cell) {
                const text = cell.textContent || cell.innerText;
                row.style.display = text.toLowerCase().includes(filter) ? "" : "none";
            }
        }
    });
});