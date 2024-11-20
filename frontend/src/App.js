import React, { useState } from "react";

function App() {
    const [hand, setHand] = useState([]); // Default to an empty array
    const [evaluation, setEvaluation] = useState("");

    const dealCards = () => {
        fetch("http://127.0.0.1:5000/api/deal")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => {
                console.log("API Response:", data); // Debugging step
                setHand(data.hand || []);
                setEvaluation(data.evaluation || "");
            })
            .catch((error) => {
                console.error("Error fetching cards:", error);
            });
    };

    return (
        <div className="App">
            <h1>Poker Game</h1>
            <button onClick={dealCards}>Deal Cards</button>
            <div>
                <h2>Your Hand:</h2>
                <ul>
                    {hand.map((card, index) => (
                        <li key={index}>{card}</li>
                    ))}
                </ul>
                <h3>{evaluation}</h3>
            </div>
        </div>
    );
}

export default App;
