import React, { useState} from 'react';
import { ResponsiveLine } from '@nivo/line';
import './App.css';

function generateData() {
  return [{
    "id": "ES",
    "data": [...Array(11).keys()].map(e => 
      ({
        "x": e + 1,
        "y": Math.random()
      })
    )
  }]
}

function App() {
  const [data, setData] = useState(generateData())

  return (
    <div className="App">
      <header className="App-header">
        <div class="App-logo">
            self
        </div>
        <div class="contain">
            <ResponsiveLine
              onClick={() => {setData(generateData())}}
              data={data}
              margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
              xScale={{ type: 'point' }}
              yScale={{ type: 'linear', stacked: true, min: 'auto', max: 'auto' }}
              axisTop={null}
              axisRight={null}
              axisBottom={{
                  orient: 'bottom',
                  tickSize: 5,
                  tickPadding: 5,
                  tickRotation: 0,
                  legend: 'transportation',
                  legendOffset: 36,
                  legendPosition: 'middle'
              }}
              axisLeft={{
                  orient: 'left',
                  tickSize: 5,
                  tickPadding: 5,
                  tickRotation: 0,
                  legend: 'count',
                  legendOffset: -40,
                  legendPosition: 'middle'
              }}
              enableGridX={false}
              enableGridY={false}
              colors={{ scheme: 'pastel2' }}
              pointSize={10}
              pointColor={{ theme: 'background' }}
              pointBorderWidth={2}
              pointBorderColor={{ from: 'serieColor' }}
              pointLabel="y"
              pointLabelYOffset={-12}
              useMesh={true}
              theme={{
                axis: {
                  ticks: {
                    text: {
                      fill: 'white'
                    }
                  }
                },
                tooltip: {
                  container: {
                    background: '#',
                    color: 'inherit',
                    fontSize: '1rem',
                    borderRadius: '2px',
                    boxShadow: '0 1px 2px rgba(0, 0, 0, 0.45)',
                    padding: '5px 9px'
                  },
                  basic: {
                    whiteSpace: 'pre',
                    display: 'flex',
                    alignItems: 'center'
                  }
                }
              }}
          />
        </div>
      </header>
    </div>
  );
}

export default App;
