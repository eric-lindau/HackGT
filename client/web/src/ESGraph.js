import React from 'react';
import { ResponsiveLine } from '@nivo/line';

const imageMap = {
  'google': 'http://pluspng.com/img-png/google-logo-png-open-2000.png',
  'facebook': 'https://facebookbrand.com/wp-content/uploads/2019/04/f_logo_RGB-Hex-Blue_512.png?w=256&h=256',
  'instagram': 'http://pluspng.com/img-png/instagram-png-instagram-png-logo-1455.png',
  'youtube': 'http://pngimg.com/uploads/youtube/youtube_PNG12.png',
}

function swag(min, activityMap) {
  return ({slice}) => {
    let x = Math.round(slice.points[0].x)
    let t = Math.round((min + x) / 95650)
    // let fake = 15721503212
    let im = []
    if (t in activityMap) {
      let d = activityMap[t].sort()
      im = d.filter((v, i) => i < 1 || d[i - 1] !== v)
    }
    return (
      <div>
        {t}
        {im.map(im => <img style={{width: '2rem', height: '2rem', margin: 'auto'}} src={imageMap[im]} alt={im}/>)}
      </div>
    )
  }
}

function ESGraph({data, legend, min, activityMap}) {
  console.log(data)
  return (
    <ResponsiveLine
        data={data}
        margin={{ top: 15, right: legend ? 110 : 10, bottom: 50, left: 60 }}
        xScale={{ type: 'point' }}
        yScale={{ type: 'linear', stacked: true, min: '0', max: '1.05' }}
        axisTop={null}
        axisRight={null}
        axisBottom={{
            orient: 'bottom',
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: 'Time',
            legendOffset: 36,
            legendPosition: 'middle',
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
        colors={{ scheme: 'nivo' }}
        pointSize={10}
        pointColor={{ theme: 'background' }}
        pointBorderWidth={2}
        pointBorderColor={{ from: 'serieColor' }}
        pointLabel="y"
        sliceTooltip={swag(min, activityMap)}
        enableSlices={'x'}
        pointLabelYOffset={-12}
        useMesh={true}
        enablePoints={false}
        enableArea={true}
        curve={'natural'}
        legends={legend ? [
          {
              anchor: 'bottom-right',
              direction: 'column',
              justify: false,
              translateX: 100,
              translateY: 0,
              itemsSpacing: 0,
              itemDirection: 'left-to-right',
              itemWidth: 80,
              itemHeight: 20,
              itemOpacity: 0.75,
              symbolSize: 12,
              symbolShape: 'circle',
              symbolBorderColor: 'rgba(0, 0, 0, .5)',
              itemTextColor: 'white',
              effects: [
                  {
                      on: 'hover',
                      style: {
                          itemBackground: 'rgba(0, 0, 0, .03)',
                          itemOpacity: 1
                      }
                  }
              ]
          }
        ] : []}
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

export default ESGraph;
