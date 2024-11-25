import React, { useState } from "react";

// Base path to the card images
const cardImagesBasePath = "/assets/cards/";

// Helper function to generate the card image path
const getCardImage = (card) => {
    // Convert card name to match the image file naming convention
    const imageName = card.toLowerCase().replace(/ /g, "_") + ".png";
    return `${cardImagesBasePath}${imageName}`;
};

function App() {
    const [hand, setHand] = useState([]);
    const [evaluation, setEvaluation] = useState("");

    const dealCards = () => {
        fetch("http://127.0.0.1:5000/api/deal")
            .then((response) => response.json())
            .then((data) => {
                setHand(data.hand || []);
                setEvaluation(data.evaluation || "");
            })
            .catch((error) => console.error("Error fetching cards:", error));
    };

    return (
        <div className="App">
            <h1>Poker Game</h1>
            <button onClick={dealCards}>Deal Cards</button>
            <div>
                <h2>Your Hand:</h2>
                <div style={{ display: "flex", gap: "10px" }}>
                    {hand.map((card, index) => (
                        <img
                            key={index}
                            src={getCardImage(card)}
                            alt={card}
                            style={{ width: "100px", height: "auto" }}
                        />
                    ))}
                </div>
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
