const { spawn } = require('child_process');

exports.handler = async function(event, context) {
  try {
    const python = spawn('python', ['../../betting_analyzer.py']);
    
    return new Promise((resolve, reject) => {
      let dataString = '';
      
      python.stdout.on('data', function(data) {
        dataString += data.toString();
      });
      
      python.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
      });
      
      python.on('close', (code) => {
        if (code !== 0) {
          reject(new Error(`Process exited with code ${code}`));
          return;
        }
        
        resolve({
          statusCode: 200,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          },
          body: JSON.stringify({
            bets: dataString
          })
        });
      });
    });
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to execute' })
    };
  }
}
