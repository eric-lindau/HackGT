import React, { useState} from 'react';
import { ResponsiveLine } from '@nivo/line';
import './App.css';

DB_ENDPOINT = ''

function getData() {
  res = await fetch(`${DB_ENDPOINT}?`)
  if (res.statusCode != 200) {
    console.log("BAD DATA")
    console.log(res)
    return []
  }
  data = res.json()
  return data
}

function generateData() {
  data = getData()
  return [{
    "id": "ES",
    "data": data.map(e => 
      ({
        "x": e.time,
        "y": e.score
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
                  legend: 'Time',
                  legendOffset: 36,
                  legendPosition: 'middle'
              }}
              axisLeft={{
                  orient: 'left',
                  tickSize: 5,
                  tickPadding: 5,
                  tickRotation: 0,
                  legend: 'Emotion Scores',
                  legendOffset: -40,
                  legendPosition: 'middle',
                  textColor: 'white'
              }}
              enableGridX={false}
              enableGridY={true}
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
                  },
                  legend: {
                    text: {
                      fill: 'white',
                      fontSize: 12
                    }
                  }
                },
                legends: {
                  text: {
                    fill: 'red'
                  }
                },
                crosshair: {
                  line: {
                    stroke: 'white',
                    strokeWidth: 1,
                    strokeOpacity: 0.75,
                    strokeDasharray: '6 6'
                  }
                },
                grid: {
                  line: {
                    stroke: 'rgba(255, 255, 255, 0.3)',
                    strokeWidth: 1
                  }
                },
                legends: {
                  text: {
                    fill: 'white'
                  }
                },
                annotations: {
                  text: {
                    color: 'white'
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
