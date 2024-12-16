import './App.css';
import React, { useState } from "react";

const cardImagesBasePath = "/assets/cards/";

const getCardImage = (card) => {
    const imageName = card.toLowerCase().replace(/ /g, "_") + ".png";
    return `${cardImagesBasePath}${imageName}`;
};

function App() {
    const [hand, setHand] = useState([]);
    const [evaluation, setEvaluation] = useState("");
    const [money, setMoney] = useState(100);
    const [freeRedealAvailable, setFreeRedealAvailable] = useState(true);
    const [payoutClaimed, setPayoutClaimed] = useState(false);
    const [payoutMessage, setPayoutMessage] = useState("");
    const [selectedCards, setSelectedCards] = useState([]);

    const dealCards = () => {
        fetch("http://127.0.0.1:5000/api/deal")
            .then(response => response.json())
            .then(data => {
                setHand(data.hand || []);
                setEvaluation(data.evaluation || "");
                setMoney(data.money);
                setFreeRedealAvailable(true); // Reset free re-deal
                setPayoutClaimed(false);
                setPayoutMessage("");
                setSelectedCards([]);
            })
            .catch(error => console.error("Error fetching cards:", error));
    };

    const redealCards = () => {
        fetch("http://127.0.0.1:5000/api/redeal", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ selectedCards })
        })
            .then(response => response.json())
            .then(data => {
                setHand(data.hand || []);
                setEvaluation(data.evaluation || "");
                setFreeRedealAvailable(data.freeRedealAvailable);
                setSelectedCards([]);
            })
            .catch(error => console.error("Error re-dealing cards:", error));
    };

    const payout = () => {
        if (payoutClaimed) return;

        fetch("http://127.0.0.1:5000/api/payout", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ evaluation })
        })
            .then(response => response.json())
            .then(data => {
                setMoney(data.money);
                setPayoutClaimed(true);
                setPayoutMessage(`You won $${data.payout} from your bet! New total: $${data.money}`);
            })
            .catch(error => console.error("Error processing payout:", error));
    };

    const toggleCardSelection = (index) => {
        setSelectedCards((prevSelected) =>
            prevSelected.includes(index)
                ? prevSelected.filter(i => i !== index)
                : [...prevSelected, index]
        );
    };

    return (
        <div className="App">
            <h1>Poker Game</h1>
            <p>Money: ${money}</p>
            <button onClick={dealCards}>Deal Cards (-$10)</button>
            <div>
                <button onClick={redealCards} disabled={!freeRedealAvailable || selectedCards.length === 0}>
                    Free Re-deal
                </button>
                <button onClick={payout} disabled={payoutClaimed || evaluation === ""}>
                    Payout
                </button>
            </div>
            <p>{payoutMessage}</p>
            <div className="cards-container">
                {hand.map((card, index) => (
                    <img
                        key={index}
                        src={getCardImage(card)}
                        alt={card}
                        className={selectedCards.includes(index) ? "selected" : ""}
                        onClick={() => toggleCardSelection(index)}
                    />
                ))}
            </div>
            <h3>{evaluation}</h3>
        </div>
    );
}

export default App;
