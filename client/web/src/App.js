import React, { useState } from 'react';

import './App.css';
import ESGraph from './ESGraph';
import logo from './logo.png';

const DB_ENDPOINT = 'https://swagv1.azurewebsites.net/api/readEScores'
const MAX_DATAPOINTS = 20

let maxTimestamp = 0
let update = true
let min = 0

async function getData(endpoint) {
  return fetch(`${endpoint}?pid=1&max_ts=${maxTimestamp}`)
    .then(data => data ? data.json() : [])
    .then(data => {
      console.log(data)
      data.sort((a, b) => a.ts - b.ts)
      console.log(data)
      // data = data.filter((v, i) => i < 1 ? true : data[i - 1].ts === v.ts)
      console.log(data.length)
      console.log(data.length - Math.min(data.length, MAX_DATAPOINTS))
      min = data[data.length - Math.min(data.length, MAX_DATAPOINTS)].ts
      return data.slice(MAX_DATAPOINTS * -1, data.length)
    })
    .catch(console.log)
}

function compileESData(data) {
  data = data.map(e => ({
      "x": e.ts - min,
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
        "x": e.ts - min,
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
      console.log(newData)
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
            <img id="logo" src={logo}></img>
        </div>
        <div className="contain">
            <ESGraph data={ESData} legend={false}/>
        </div>
        <div className="contain">
            <ESGraph data={EmotionData} legend={true}/>
        </div>
      </header>
    </div>
  );
}

export default App;
