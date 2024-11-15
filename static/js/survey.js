document.getElementById("surveyForm").onsubmit = async function(event) {
    event.preventDefault();

    // Show the loading spinner
    document.getElementById("loadingSpinner").style.display = "block";

    const userId = document.getElementById("userId").value;

    // Validate User ID
    const userIdPattern = /^[a-zA-Z0-9_]{5,}$/;
    if (!userIdPattern.test(userId)) {
        document.getElementById("responseMessage").innerText = "Invalid User ID. Must be at least 5 characters and alphanumeric (underscores allowed).";
        return;
    }

    // Gather survey results
    const surveyResults = [];
    for (let i = 1; i <= 10; i++) {
        const selectedOption = document.querySelector(`input[name="survey_results_${i}"]:checked`);
        if (selectedOption) {
            surveyResults.push({ question_number: i, question_value: parseInt(selectedOption.value) });
        } else {
            document.getElementById("responseMessage").innerText = `Please answer all questions. Question ${i} is missing.`;
            return;
        }
    }

    // Submit data to server
    const response = await fetch("/process-survey", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, survey_results: surveyResults })
    });

    const result = await response.json();
    const messageElement = document.getElementById("responseMessage");

    if (response.ok) {
        document.getElementById("loadingSpinner").style.display = "none";
        messageElement.innerText = "Survey submitted successfully!";
        displayResults(result);

        // Show the reset button after successful submission
        document.getElementById("resetButton").style.display = "inline-block";

    } else {
        messageElement.innerText = result.error || "There was an error submitting the survey.";
    }
};

function displayResults(data) {
    const resultsSection = document.getElementById("resultsSection");
    resultsSection.innerHTML = "";  // Clear any previous results

    if (data.status === "success") {
        const rowDiv = document.createElement("div");
        rowDiv.classList.add("row");

        // Survey Analysis Section
        const analysisCol = document.createElement("div");
        analysisCol.classList.add("col-md-6", "mb-4");

        const analysisTitle = document.createElement("h5");
        analysisTitle.classList.add("text-center");
        analysisTitle.innerText = "Survey Analysis";
        analysisCol.appendChild(analysisTitle);

        const analysisList = document.createElement("ul");
        analysisList.classList.add("list-group");

        for (const [key, value] of Object.entries(data.analysis)) {
            const listItem = document.createElement("li");
            listItem.classList.add("list-group-item", "text-left");
            listItem.innerHTML = `<strong>${titleCase(key)}:</strong> ${value}`;
            analysisList.appendChild(listItem);
        }
        analysisCol.appendChild(analysisList);
        rowDiv.appendChild(analysisCol);

        // Survey Statistics Section
        const statisticsCol = document.createElement("div");
        statisticsCol.classList.add("col-md-6", "mb-4");

        const statisticsTitle = document.createElement("h5");
        statisticsTitle.classList.add("text-center");
        statisticsTitle.innerText = "Survey Statistics";
        statisticsCol.appendChild(statisticsTitle);

        const statisticsList = document.createElement("ul");
        statisticsList.classList.add("list-group");

        for (const [key, value] of Object.entries(data.statistics)) {
            const listItem = document.createElement("li");
            listItem.classList.add("list-group-item", "text-left");
            listItem.innerHTML = `<strong>${titleCase(key)}:</strong> ${value}`;
            statisticsList.appendChild(listItem);
        }
        statisticsCol.appendChild(statisticsList);
        rowDiv.appendChild(statisticsCol);

        resultsSection.appendChild(rowDiv);
    } else {
        const errorTitle = document.createElement("p");
        errorTitle.classList.add("text-danger", "text-center");
        errorTitle.innerText = "There was an error processing the survey.";
        resultsSection.appendChild(errorTitle);
    }
}

// Helper function to convert text to title case
function titleCase(str) {
    return str.replace(/_/g, ' ').replace(/\w\S*/g, (txt) => txt.charAt(0).toUpperCase() + txt.slice(1).toLowerCase());
}

// Script to reset the form and clear results
document.getElementById("resetButton").onclick = function() {
    // Reset the form
    document.getElementById("surveyForm").reset();

    // Clear any displayed messages or results
    document.getElementById("responseMessage").innerText = "";
    document.getElementById("resultsSection").innerHTML = "";

    // Hide the reset button again
    document.getElementById("resetButton").style.display = "none";
};
