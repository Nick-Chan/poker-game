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
    const [payoutClaimed, setPayoutClaimed] = useState(true); // Start as true to allow the first deal
    const [payoutMessage, setPayoutMessage] = useState("");
    const [selectedCards, setSelectedCards] = useState([]);

    const dealCards = () => {
        if (!payoutClaimed) {
            console.error("Payout must be claimed before dealing a new hand.");
            return;
        }

        fetch("http://127.0.0.1:5000/api/deal")
            .then((response) => {
                if (!response.ok) {
                    return response.json().then((err) => Promise.reject(err));
                }
                return response.json();
            })
            .then((data) => {
                setHand(data.hand || []);
                setEvaluation(data.evaluation || "");
                setMoney(data.money);
                setFreeRedealAvailable(true);
                setPayoutClaimed(false); // Disable deal button until payout is claimed
                setPayoutMessage("Select cards to a re-deal, or click payout to end the turn!");
                setSelectedCards([]);
                console.log("Deal successful:", data); // Debugging log
            })
            .catch((error) => {
                console.error("Error dealing cards:", error);
            });
    };

    const redealCards = () => {
        fetch("http://127.0.0.1:5000/api/redeal", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ selectedCards }),
        })
            .then((response) => {
                if (!response.ok) {
                    return response.json().then((err) => Promise.reject(err));
                }
                return response.json();
            })
            .then((data) => {
                if (data.error) {
                    console.error(data.error);
                    return;
                }
                // Update the hand and evaluation after re-deal
                setHand(data.hand || []);
                setEvaluation(data.evaluation || "");
                setFreeRedealAvailable(data.freeRedealAvailable);
                setSelectedCards([]);

                // Automatically initiate payout
                payoutAfterRedeal(data.evaluation);      
            })
            .catch((error) => {
                console.error("Error re-dealing cards:", error);
            });
    };

    const payout = () => {
        if (payoutClaimed) {
            console.error("Payout already claimed.");
            return;
        }

        fetch("http://127.0.0.1:5000/api/payout", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ evaluation }),
        })
            .then((response) => {
                if (!response.ok) {
                    return response.json().then((err) => Promise.reject(err));
                }
                return response.json();
            })
            .then((data) => {
                if (data.error) {
                    console.error(data.error);
                    return;
                }
                setMoney(data.money); // Update money with payout
                setPayoutClaimed(true); // Allow deal button after payout
                setPayoutMessage(`You won $${data.payout} from your bet! New total: $${data.money}`);
                console.log("Payout successful:", data); // Debugging log
            })
            .catch((error) => {
                console.error("Error processing payout:", error);
            });
    };

    const payoutAfterRedeal = (evaluation) => {
        fetch("http://127.0.0.1:5000/api/payout", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ evaluation }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.error) {
                    console.error(data.error);
                    return;
                }
    
                // Update money and payout message
                setMoney(data.money);
                setPayoutClaimed(true); // Allow deal button after payout
                setPayoutMessage(`You won $${data.payout} from your re-deal! New total: $${data.money}`);
                console.log("Payout successful after re-deal:", data);
            })
            .catch((error) => {
                console.error("Error processing payout after re-deal:", error);
            });
    };

    const toggleCardSelection = (index) => {
        setSelectedCards((prevSelected) =>
            prevSelected.includes(index)
                ? prevSelected.filter((i) => i !== index)
                : [...prevSelected, index]
        );
    };

    return (
        <div className="App">
                {/* Payout Info Icon */}
            <div className="payout-info" title="View payouts">
                ?
                <div className="tooltip">
                <p><strong>Payouts:</strong></p>
                <ul style={{ listStyleType: "none", padding: 0 }}>
                    <li>Straight Flush: 25x</li>
                    <li>Four of a Kind: 15x</li>
                    <li>Full House: 10x</li>
                    <li>Flush: 5x</li>
                    <li>Straight: 4x</li>
                    <li>Three of a Kind: 3x</li>
                    <li>Two Pair: 2x</li>
                    <li>Pair: 1x</li>
                    <li>High Card (A or K): 1x</li>
                    <li>Anything else: 0x</li>
                </ul>
                </div>
            </div>
            
            {/* Game content */}
            <h1>Poker Game</h1>
            <p>Money: ${money}</p>
            <button onClick={dealCards} disabled={!payoutClaimed}>
                Deal Cards (-$10)
            </button>
            <div>
                <button
                    onClick={redealCards}
                    disabled={!freeRedealAvailable || selectedCards.length === 0}
                >
                    Free Re-deal
                </button>
                <button
                    onClick={payout}
                    disabled={payoutClaimed || evaluation === ""}
                >
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
