// Initialize WebSocket connection
const ws = new WebSocket("ws://ec2-54-208-250-172.compute-1.amazonaws.com/ws/orders");

// Handle incoming messages
ws.onmessage = function(event) {
    const order = JSON.parse(event.data);
    const tableBody = document.querySelector("table tbody");

    // Create a new row for the order
    const newRow = document.createElement("tr");
    newRow.innerHTML = `
        <td>${order.symbol}</td>
        <td>${order.price}</td>
        <td>${order.quantity}</td>
        <td>${order.order_type}</td>
    `;

    // Add the new row to the table
    tableBody.appendChild(newRow);
};

// Handle WebSocket connection open
ws.onopen = function() {
    console.log("WebSocket connection established");
};

// Handle WebSocket connection close
ws.onclose = function() {
    console.log("WebSocket connection closed");
};

// Handle WebSocket errors
ws.onerror = function(error) {
    console.error("WebSocket error:", error);
};