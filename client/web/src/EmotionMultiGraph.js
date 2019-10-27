/* eslint react/prop-types: 0 */
import React from 'react';
import { ResponsiveBump } from '@nivo/bump';

function EmotionMultiGraph({data}) {
  // let dat = [
  //   {
  //     "id": "Serie 1",
  //     "data": [
  //       {
  //         "x": 2000,
  //         "y": 5
  //       },
  //       {
  //         "x": 2001,
  //         "y": 12
  //       },
  //       {
  //         "x": 2002,
  //         "y": 2
  //       },
  //       {
  //         "x": 2003,
  //         "y": 12
  //       },
  //       {
  //         "x": 2004,
  //         "y": 12
  //       }
  //     ]
  //   },
  //   {
  //     "id": "Serie 2",
  //     "data": [
  //       {
  //         "x": 2000,
  //         "y": 2
  //       },
  //       {
  //         "x": 2001,
  //         "y": 11
  //       },
  //       {
  //         "x": 2002,
  //         "y": 6
  //       },
  //       {
  //         "x": 2003,
  //         "y": 1
  //       },
  //       {
  //         "x": 2004,
  //         "y": 3
  //       }
  //     ]
  //   },
  //   {
  //     "id": "Serie 3",
  //     "data": [
  //       {
  //         "x": 2000,
  //         "y": 10
  //       },
  //       {
  //         "x": 2001,
  //         "y": 5
  //       },
  //       {
  //         "x": 2002,
  //         "y": 12
  //       },
  //       {
  //         "x": 2003,
  //         "y": 8
  //       },
  //       {
  //         "x": 2004,
  //         "y": 8
  //       }
  //     ]
  //   },
  //   {
  //     "id": "Serie 4",
  //     "data": [
  //       {
  //         "x": 2000,
  //         "y": 7
  //       },
  //       {
  //         "x": 2001,
  //         "y": 4
  //       },
  //       {
  //         "x": 2002,
  //         "y": 5
  //       },
  //       {
  //         "x": 2003,
  //         "y": 5
  //       },
  //       {
  //         "x": 2004,
  //         "y": 1
  //       }
  //     ]
  //   },
  //   {
  //     "id": "Serie 5",
  //     "data": [
  //       {
  //         "x": 2000,
  //         "y": 9
  //       },
  //       {
  //         "x": 2001,
  //         "y": 1
  //       },
  //       {
  //         "x": 2002,
  //         "y": 4
  //       },
  //       {
  //         "x": 2003,
  //         "y": 10
  //       },
  //       {
  //         "x": 2004,
  //         "y": 5
  //       }
  //     ]
  //   },
  //   {
  //     "id": "Serie 8",
  //     "data": [
  //       {
  //         "x": 2000,
  //         "y": 4
  //       },
  //       {
  //         "x": 2001,
  //         "y": 7
  //       },
  //       {
  //         "x": 2002,
  //         "y": 10
  //       },
  //       {
  //         "x": 2003,
  //         "y": 6
  //       },
  //       {
  //         "x": 2004,
  //         "y": 13
  //       }
  //     ]
  //   }
  // ]

  // let dat2 = [{"id": "1", "data": [{"x": 1, "y": 2}, {"x": 2, "y": 3}, {"x": 3, "y": 3}]},
  // {"id": "2", "data": [{"x": 1, "y": 4}, {"x": 2, "y": 11}, {"x": 3, "y": 4}]},
  // {"id": "3", "data": [{"x": 1, "y": 10}, {"x": 2, "y": 20}, {"x": 3, "y": 5}]}]

  return (
    <ResponsiveBump
          data={data}
          margin={{ top: 40, right: 100, bottom: 40, left: 60 }}
          colors={{ scheme: 'spectral' }}
          lineWidth={3}
          activeLineWidth={6}
          inactiveLineWidth={3}
          inactiveOpacity={0.15}
          pointSize={10}
          activePointSize={16}
          inactivePointSize={0}
          pointColor={{ theme: 'background' }}
          pointBorderWidth={3}
          activePointBorderWidth={3}
          pointBorderColor={{ from: 'pastel1' }}
          axisTop={{
              tickSize: 5,
              tickPadding: 5,
              tickRotation: 0,
              legend: '',
              legendPosition: 'middle',
              legendOffset: -36
          }}
          axisRight={null}
          axisBottom={{
              tickSize: 5,
              tickPadding: 5,
              tickRotation: 0,
              legend: '',
              legendPosition: 'middle',
              legendOffset: 32
          }}
          axisLeft={{
              tickSize: 5,
              tickPadding: 5,
              tickRotation: 0,
              legend: 'ranking',
              legendPosition: 'middle',
              legendOffset: -40
          }}
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
  )
}

export default EmotionMultiGraph;
