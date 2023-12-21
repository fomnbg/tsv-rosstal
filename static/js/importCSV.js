// inzwischen obsolete, da die Daten direkt via Python in die HTML-Tabelle eingefügt werden
// nur zu Demonstrationszwecken hier belassen

fetch('/static/fileAblage/data.csv')
    .then(response => response.text())
    .then(csvText => {
        const rows = csvText.split('\n').map(row => row.split(';'));
        const tableBody = document.getElementById('table1').getElementsByTagName('tbody')[0];
        const insertPoint = document.getElementById('csv-insert-point');

        rows.forEach((rowData, index) => {
            if (index > 0 && rowData.length > 1) { // Skip header row and empty rows
                let row = document.createElement('tr');
                rowData.forEach((cellData) => {
                    let cell = row.insertCell();
                    cell.innerHTML = cellData.trim();
                });
                tableBody.insertBefore(row, insertPoint);
            }
        });
    })
    .catch(error => console.error('Error:', error));
