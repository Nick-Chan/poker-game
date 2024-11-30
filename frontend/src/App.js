import './App.css';
import React, { useState } from "react";

// Base path to card images
const cardImagesBasePath = "/assets/cards/";

// Helper function to get card image path
const getCardImage = (card) => {
    const imageName = card.toLowerCase().replace(/ /g, "_") + ".png";
    return `${cardImagesBasePath}${imageName}`;
};

function App() {
    const [hand, setHand] = useState([]);
    const [evaluation, setEvaluation] = useState("");
    const [selectedCards, setSelectedCards] = useState([]); // Track selected cards

    // Fetch new cards from the backend
    const dealCards = () => {
        fetch("http://127.0.0.1:5000/api/deal")
            .then((response) => response.json())
            .then((data) => {
                setHand(data.hand || []);
                setEvaluation(data.evaluation || "");
                setSelectedCards([]); // Reset selections after a new deal
            })
            .catch((error) => console.error("Error fetching cards:", error));
    };

    // Redeal selected cards
    const redealCards = () => {
        fetch("http://127.0.0.1:5000/api/redeal", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ selectedCards }),
        })
            .then((response) => response.json())
            .then((data) => {
                setHand(data.hand || []);
                setEvaluation(data.evaluation || "");
                setSelectedCards([]); // Reset selections after re-deal
            })
            .catch((error) => console.error("Error re-dealing cards:", error));
    };

    // Toggle card selection
    const toggleCardSelection = (index) => {
        setSelectedCards((prevSelected) =>
            prevSelected.includes(index)
                ? prevSelected.filter((i) => i !== index) // Deselect card
                : [...prevSelected, index] // Select card
        );
    };

    return (
        <div className="App">
            <h1>Poker Game</h1>
            <button onClick={dealCards}>Deal Cards</button>
            <button
                onClick={redealCards}
                disabled={selectedCards.length === 0} // Disable if no cards are selected
            >
                Re-deal Selected Cards
            </button>
            <div className="cards-container">
                {hand.map((card, index) => (
                    <img
                        key={index}
                        src={getCardImage(card)}
                        alt={card}
                        className={selectedCards.includes(index) ? "selected" : ""}
                        onClick={() => toggleCardSelection(index)} // Select/deselect cards
                    />
                ))}
            </div>
            <h3>{evaluation}</h3>
        </div>
    );
}

export default App;
