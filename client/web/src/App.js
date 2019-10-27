import React, { useState } from 'react';

import './App.css';
import ESGraph from './ESGraph';
import EmotionMultiGraph from './EmotionMultiGraph';

const DB_ENDPOINT = 'https://swagv1.azurewebsites.net/api/readEScores'
const MAX_DATAPOINTS = 35

let maxTimestamp = 0
let update = true

async function getData(endpoint) {
  return fetch(`${endpoint}?pid=1&max_ts=${maxTimestamp}`)
    .then(data => data ? data.json() : [])
    .then(data => {
      data.sort((a, b) => a.ts - b.ts)
      let min = data.length >= MAX_DATAPOINTS ?
        data[data.length - MAX_DATAPOINTS].ts : (data.length > 0 ? data[0].ts : 0)
      data.forEach(e => { e.ts -= min })

      return data.length >= MAX_DATAPOINTS ? data.slice(data.length - MAX_DATAPOINTS, data.length + 1) : data
    })
    .catch(console.log)
}

function compileESData(data) {
  data = data.map(e => ({
      "x": e.ts,
      "y": parseFloat(e.value)
    })
  )
  
  return data && data.length > 0 ? [{
    "id": "E Score",
    "data": data
  }] : []
}

function compileEmotionData(data) {
  if (!data || data.length === 0) {
    return []
  }
  let emotions = {}
  data.forEach(e => {
    let obj = JSON.parse(e.data).faceAttributes.emotion
    Object.keys(obj).forEach(key => {
      let n = {
        "x": e.ts,
        "y": obj[key]
      }
      if (!(key in emotions)) {
        emotions[key] = []
      } else {
        emotions[key].push(n)
      }
    })
  })
  let res = []
  Object.keys(emotions).forEach(key => {
    if (key in emotions && emotions[key].length > 0) {
      res.push({
        "id": key,
        "data": emotions[key]
      })
    }
  })
  return res
}

function App() {
  const [ESData, setESData] = useState([])
  const [EmotionData, setEmotionData] = useState([])

  function updateData() {
    getData(DB_ENDPOINT).then(newData => {
      if (!newData) {
        return
      }
      let compiledES = compileESData(newData)
      let compiledEmotions = compileEmotionData(newData)
      setESData(compiledES)
      setEmotionData(compiledEmotions)
    })
  }

  if (update) {
    update = false
    setTimeout(function tick() {updateData(); setTimeout(tick, 3000)}, 3000)
  }

  return (
    <div className="App">
      <header className="App-header">
        <div className="App-logo">
            self
        </div>
        <div className="contain">
            <ESGraph data={ESData}/>
        </div>
        <div className="contain">
            <EmotionMultiGraph data={EmotionData}/>
        </div>
      </header>
    </div>
  );
}

export default App;
