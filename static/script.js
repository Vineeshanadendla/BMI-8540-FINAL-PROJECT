document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('uploadForm');
    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const formData = new FormData(form);
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (data.type_counts && data.category_counts) {
            renderCharts(data);
            renderDataInfo(data);
        } else {
            alert("Error uploading or processing file.");
        }
    });
});

function renderCharts(data) {
    const typeCtx = document.getElementById('typeChart').getContext('2d');
    const categoryCtx = document.getElementById('categoryChart').getContext('2d');

    new Chart(typeCtx, {
        type: 'bar',
        data: {
            labels: Object.keys(data.type_counts),
            datasets: [{
                label: 'Type Distribution',
                data: Object.values(data.type_counts),
                backgroundColor: 'skyblue'
            }]
        }
    });

    new Chart(categoryCtx, {
        type: 'pie',
        data: {
            labels: Object.keys(data.category_counts),
            datasets: [{
                data: Object.values(data.category_counts),
                backgroundColor: ['#ff6384','#36a2eb','#ffce56','#8bc34a','#9c27b0']
            }]
        }
    });
}

function renderDataInfo(data) {
    document.getElementById('dataInfo').innerHTML = `
        <h4>Data Summary:</h4>
        <ul>
            <li><strong>Total Bacterial Types:</strong> ${Object.keys(data.type_counts).length}</li>
            <li><strong>Total Categories:</strong> ${Object.keys(data.category_counts).length}</li>
            <li><strong>Bacterial Types:</strong> ${Object.keys(data.type_counts).join(', ')}</li>
            <li><strong>Categories:</strong> ${Object.keys(data.category_counts).join(', ')}</li>
        </ul>
    `;
}