function escapeHtml(text) {
    return String(text)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;");
}

// "55.6%", or a dash when there is no value (e.g. no matches in that category)
function formatPercent(rate) {
    if (rate == null) return "–";
    return `${(rate * 100).toFixed(1)}%`;
}

async function loadPlayers() {
    const [recordsResponse, playersResponse] = await Promise.all([
        fetch("data/player_records.json"),
        fetch("data/players.json")
    ]);

    const records = await recordsResponse.json();
    const players = await playersResponse.json();

    // Lookup table: player ID -> player name
    const playerNames = {};
    players.forEach(player => {
        playerNames[player.id] = player.name;
    });

    // Sort by match win rate, highest first
    records.sort((a, b) => b.match_win_rate - a.match_win_rate);

    let html = `
        <div class="table-wrap">
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Player</th>
                    <th>Drafts</th>
                    <th>Matches</th>
                    <th>W-L-D</th>
                    <th>Match win %</th>
                    <th title="Match win % when on the play in game 1">Play win %</th>
                    <th title="Match win % when on the draw in game 1">Draw win %</th>
                    <th>Game W-L</th>
                    <th>Game win %</th>
                </tr>
            </thead>
            <tbody>
    `;

    records.forEach((record, index) => {
        const name = escapeHtml(playerNames[record.player] ?? `Player ${record.player}`);

        html += `
            <tr>
                <td>${index + 1}</td>
                <td>${name}</td>
                <td>${record.drafts}</td>
                <td>${record.n_matches}</td>
                <td>${record.match_wins}-${record.match_losses}-${record.match_draws}</td>
                <td>${formatPercent(record.match_win_rate)}</td>
                <td>${formatPercent(record.winrate_g1_play)}</td>
                <td>${formatPercent(record.winrate_g1_draw)}</td>
                <td>${record.game_wins}-${record.game_losses}</td>
                <td>${formatPercent(record.game_win_rate)}</td>
            </tr>
        `;
    });

    html += `
            </tbody>
        </table>
        </div>
    `;

    document.getElementById("players-table").innerHTML = html;
}

loadPlayers();