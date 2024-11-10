async function analyzeUrl() {
    const urlInput = document.getElementById('url').value;
    const topNInput = document.getElementById('topN').value || 10;  
    
    if (!urlInput) {
        alert("Please enter a URL");
        return;
    }

    const response = await fetch("/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: urlInput, n: parseInt(topNInput) })
    });

    if (response.ok) {
        const data = await response.json();
        displayResults(data.top_words);
    } else {
        alert("Error fetching or analyzing the URL");
    }
}

function displayResults(topWords) {
    const resultsTable = document.getElementById("resultsTable");
    const resultsBody = document.getElementById("resultsBody");

    resultsBody.innerHTML = ""; 

    topWords.forEach(([word, frequency]) => {
        const row = document.createElement("tr");
        row.innerHTML = `<td>${word}</td><td>${frequency}</td>`;
        resultsBody.appendChild(row);
    });

    resultsTable.style.display = "table";
}
