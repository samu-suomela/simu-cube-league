
async function loadHeadToHead() {
    try {
        // Load JSON files
        const [recordsResponse, playersResponse] = await Promise.all([
            fetch("data/head_to_head.json"),
            fetch("data/players.json")
        ]);

        if (!recordsResponse.ok || !playersResponse.ok) {
            throw new Error("Could not load JSON files");
        }

        const records = await recordsResponse.json();
        const players = await playersResponse.json();

        // Create player ID -> name lookup
        const playerNames = {};

        players.forEach(player => {
            playerNames[player.id] = player.name;
        });

        // Populate player dropdown
        const select = document.getElementById("player-select");

        players.forEach(player => {
            const option = document.createElement("option");
            option.value = player.id;
            option.textContent = player.name;
            select.appendChild(option);
        });

        // Update table when selection changes
        select.addEventListener("change", () => {
            displayHeadToHead(records, playerNames, Number(select.value));
        });

    } catch (error) {
        console.error("Error loading head-to-head data:", error);

        document.getElementById("head-to-head-table").textContent =
            "Could not load head-to-head statistics.";
    }
}


function displayHeadToHead(records, playerNames, playerId) {
    const container = document.getElementById("head-to-head-table");

    // Get records for selected player
    const playerRecords = records.filter(
        record => record.player === playerId
    );

    // Sort by match win rate
    playerRecords.sort(
        (a, b) => b.match_win_rate - a.match_win_rate
    );

    // Build table
    let html = `
        <table>
            <thead>
                <tr>
                    <th>Opponent</th>
                    <th>Matches</th>
                    <th>Match W-L-D</th>
                    <th>Match win %</th>
                    <th>Game W-L</th>
                    <th>Game win %</th>
                </tr>
            </thead>
            <tbody>
    `;

    playerRecords.forEach(record => {
        const opponentName =
            playerNames[record.opponent] ?? `Player ${record.opponent}`;

        html += `
            <tr>
                <td>${opponentName}</td>
                <td>${record.n_matches}</td>
                <td>${record.match_wins}-${record.match_losses}-${record.match_draws}</td>
                <td>${(record.match_win_rate * 100).toFixed(1)}%</td>
                <td>${record.game_wins}-${record.game_losses}</td>
                <td>${(record.game_win_rate * 100).toFixed(1)}%</td>
            </tr>
        `;
    });

    html += `
            </tbody>
        </table>
    `;

    if (playerRecords.length === 0) {
        container.textContent = "No head-to-head records found.";
    } else {
        container.innerHTML = html;
    }
}


// Start application
loadHeadToHead();
