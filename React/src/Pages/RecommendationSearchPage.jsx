.recommendation-search-page {
    max-width: 900px; /* Constrain width */
    margin: 0 auto;
    padding: 20px;
    text-align: left;
    padding-top: 80px; /* Adjust for navbar */
}

.mode-buttons {
    display: flex;
    justify-content: space-evenly;
    margin-bottom: 20px;
}

.mode-buttons button {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    background-color: rebeccapurple;
    color: white;
}

.mode-buttons button.active {
    background-color: purple;
    font-weight: bold;
}

.mode-buttons button:hover {
    background-color: darkorchid;
}

.recommendation-content {
    margin-top: 20px;
}

.recommendations {
    margin-top: 20px; /* Space above recommendations */
    border: 1px solid #ddd;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}
