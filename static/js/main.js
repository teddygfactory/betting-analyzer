document.addEventListener('DOMContentLoaded', function() {
    fetchBettingOpportunities();
});

async function fetchBettingOpportunities() {
    try {
        const response = await fetch('/.netlify/functions/get_bets');
        const data = await response.json();
        
        // Parse the betting opportunities from the response
        const betsContainer = document.getElementById('bettingOpportunities');
        const bets = parseBets(data.bets);
        
        if (bets.length === 0) {
            betsContainer.innerHTML = '<p>No betting opportunities available at the moment.</p>';
            return;
        }
        
        // Display the betting opportunities
        betsContainer.innerHTML = bets.map(bet => `
            <div class="bet-item">
                <h3>${bet.sport} - ${bet.time}</h3>
                <div class="bet-details">
                    <p><strong>Matchup:</strong> ${bet.matchup}</p>
                    <p><strong>Bet Type:</strong> ${bet.betType}</p>
                    <p><strong>Pick:</strong> ${bet.pick}</p>
                    <p><strong>Analysis:</strong> ${bet.analysis}</p>
                    <p class="value-indicator">Expected Value: ${bet.expectedValue}</p>
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Error fetching betting opportunities:', error);
        document.getElementById('bettingOpportunities').innerHTML = 
            '<p>Error loading betting opportunities. Please try again later.</p>';
    }
}

function parseBets(betsString) {
    // Split the string into lines
    const lines = betsString.split('\n');
    const bets = [];
    let currentBet = {};
    
    for (const line of lines) {
        if (line.includes('Matchup:')) {
            if (Object.keys(currentBet).length > 0) {
                bets.push({...currentBet});
            }
            currentBet = {};
            const [sport, time] = line.split(' - ');
            currentBet.sport = sport.trim();
            currentBet.time = time.trim();
        } else if (line.includes('@')) {
            currentBet.matchup = line.trim();
        } else if (line.includes('Bet Type:')) {
            currentBet.betType = line.split(':')[1].trim();
        } else if (line.includes('Pick:')) {
            currentBet.pick = line.split(':')[1].trim();
        } else if (line.includes('Analysis:')) {
            currentBet.analysis = line.split(':')[1].trim();
        } else if (line.includes('Expected Value:')) {
            currentBet.expectedValue = line.split(':')[1].trim();
        }
    }
    
    if (Object.keys(currentBet).length > 0) {
        bets.push({...currentBet});
    }
    
    return bets;
}
