async function loadRiskData() {
    try {
        const response = await fetch("http://127.0.0.1:8000/risk");

        if (!response.ok) {
            throw new Error("API connection failed");
        }

        const data = await response.json();

        document.getElementById("status").textContent = data.status;
        document.getElementById("rainfall-risk").textContent = data.rainfall_risk;
        document.getElementById("inundation-risk").textContent = data.inundation_risk;

    } catch (error) {
        console.error(error);
        document.getElementById("status").textContent = "API OFFLINE";
    }
}

loadRiskData();