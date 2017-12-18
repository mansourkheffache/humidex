
// Construct the chart


window.onload = function()
{
//array of charts
humidexchart=[];


Array.prototype.zip = function (arr) {
    return this.map(function (e, i) {
        return [e, arr[i]];
    })
};

//webSocket initialization
ws = new WebSocket("ws://localhost:9999/websocket");
ws.onopen = function() {
    var req = {
        'type': 'query',
        'time': 4500
    };
    ws.send(JSON.stringify(req));
};

ws.onmessage = function (evt) {
    var res = JSON.parse(evt.data);
    updateDiagram(res);        
};

setInterval(callServer,10000);

diagramComfort=document.getElementById('main-first');
humidexchart[1]=new Highcharts.chart( {
    chart: {
        renderTo: diagramComfort,
        height: 400,
        zoomType:'x',
        animation:false
    },
    title: {
        text: 'Comfort Diagram'
    },   
    subtitle: {
        text: 'Temperature, Humidity, Humidex, Comfort Level'
    },
    xAxis: {
        type: 'datetime',
        //offset: 40
        crosshair:true
    },

    plotOptions: {
        series: {
            //pointStart: Date.UTC(2017, 0, 29),
            //pointInterval: 36e5
        }
    },

    series: [
    {
        type: 'line',
        useHTML:'true',
        //keys: ['y', 'rotation'], // rotation is not used here
        data: [
        ],
        color: Highcharts.getOptions().colors[3],
        fillColor:'#2f7ed8',
        name: 'amir humidex emojis',
        tooltip: {
            //valueSuffix: ' m/s'
        }
    }
    ]//end of series

});



diagramFirst=document.getElementById('detail-first');

humidexchart[2]=new Highcharts.chart( {
    chart: {
        renderTo: diagramFirst,
        height: 400,
        zoomType:'x',
         animation:false

    },
    xAxis: {
        type: 'datetime',
        //offset: 40
        crosshair:true
    },
    yAxis:[{ // Primary yAxis
          labels: {
             format: '{value} g ',
             style: {
                color: Highcharts.getOptions().colors[2]
             }
          },
          title: {
             text: 'CO2 Emitted',
             style: {
                color: Highcharts.getOptions().colors[2]
             }
          },
          opposite: true
        },
        { // Secondary yAxis
          title: {
             text: 'Emission Speed',
             style: {
                color: Highcharts.getOptions().colors[0]
             }
          },
          labels: {
             format: '{value} g/s',
             style: {
                color: Highcharts.getOptions().colors[0]
             }
          }
       }
       ],
    // boost: {
    //     useGPUTranslations: true
    // },
    title:{
        text:'CO2 emission'
    },
    xAxis: {
        //type: 'datetime',
        //offset: 40,
    },

    series: [
    {
        type: 'column',
        zoomType: 'x',
        panning: true,
        panKey: 'shift',
        yAxis:0,
        data: [
 
        ],
        fillColor:'#2f7ed8',
        name: 'CO2 Emitted',
        tooltip: {
            valueSuffix: '  Gram per Second'
        },

    },



    {
        type: 'line',
        useHTML:'true',
        yAxis:1,
        data: [

        ],
        fillColor:'#2f7ed8',
        name: 'CO2 emission speed',
        tooltip: {
            valueSuffix: '  Gram per Second'
        }
    }
    ]//end of series

});





////////Humidex chart
diagramSecond=document.getElementById('detail-second');

humidexchart[3]=new Highcharts.chart( {
    chart: {
        renderTo: diagramSecond,
        height: 400,
        zoomType:'x',
        animation:false

    },
        xAxis: {
        type: 'datetime',
        //offset: 40
        crosshair:true
    },
    yAxis:[{ // Primary yAxis
          labels: {
             format: '{value} C',
             style: {
                color: Highcharts.getOptions().colors[2]
             }
          },
          title: {
             text: 'Temperature',
             style: {
                color: Highcharts.getOptions().colors[2]
             }
          },
          opposite: true
        },
        { // Secondary yAxis
          title: {
             text: 'Humidity',
             style: {
                color: Highcharts.getOptions().colors[0]
             }
          },
          labels: {
             format: '{value} %',
             style: {
                color: Highcharts.getOptions().colors[0]
             }
          }
       },
       { // third y axis
          title: {
             text: 'Humidex Level',
             style: {
                color: Highcharts.getOptions().colors[1]
             }
          },
          labels: {
             format: ' {value}',
             style: {
                color: Highcharts.getOptions().colors[1]
             }
          }
       }
       ],
    // boost: {
    //     useGPUTranslations: true
    // },
    title:{
        text:'Temperature/Humidity/Humidex'
    },
    xAxis: {
        //type: 'datetime',
        //offset: 40,
    },

    series: [
    {
        type: 'column',
        zoomType: 'x',
        panning: true,
        panKey: 'shift',
        yAxis:0,
        data: [

        ],
        fillColor:'#2f7ed8',
        name: 'Temperature',
        tooltip: {
            valueSuffix: ' C'
        },

    },

    {
        type: 'line',
        useHTML:'true',
        yAxis:1,
        data: [
 
        ],
        fillColor:'#2f7ed8',
        name: 'Humidity',
        tooltip: {
            valueSuffix: ' %'
        }
    },

    {
        type: 'line',
        useHTML:'true',
        yAxis:2,
        data: [

        ],
        fillColor:'#2f7ed8',
        name: 'Humidex Level',
        tooltip: {
            valueSuffix: ' Humidex Index'
        }
    }
    ]//end of series

});



//power/traffic/energy chart
diagramThrid=document.getElementById('detail-third');
humidexchart[4]=new Highcharts.chart( {
    chart: {
        renderTo: diagramThrid,
        height: 400,
        zoomType:'x',
        animation:false

    },
        xAxis: {
        type: 'datetime',
        //offset: 40
        crosshair:true
    },
    yAxis:[{ // Primary yAxis
          labels: {
             format: '{value} Watts',
             style: {
                color: Highcharts.getOptions().colors[2]
             }
          },
          title: {
             text: 'Power',
             style: {
                color: Highcharts.getOptions().colors[2]
             }
          },
          opposite: true
        },
        { // Secondary yAxis
          title: {
             text: 'Traffic',
             style: {
                color: Highcharts.getOptions().colors[0]
             }
          },
          labels: {
             format: '{value} bits',
             style: {
                color: Highcharts.getOptions().colors[0]
             }
          }
       },
        { // third yAxis
          title: {
             text: 'Energy',
             style: {
                color: Highcharts.getOptions().colors[1]
             }
          },
          labels: {
             format: '{value} J',
             style: {
                color: Highcharts.getOptions().colors[1]
             }
          }
       }
       ],
    // boost: {
    //     useGPUTranslations: true
    // },
    title:{
        text:'Power/Traffic'
    },
    xAxis: {
        //type: 'datetime',
        //offset: 40,
    },

    series: [

    {
        type: 'line',
        useHTML:'true',
        yAxis:0,
        data: [

        ],
        //fillColor:'#2f7ed8',
        name: 'Power',
        tooltip: {
            valueSuffix: '  J'
        }
    },
    {
        type: 'line',
        useHTML:'true',
        yAxis:1,
        data: [

        ],
        //fillColor:'#2f7ed8',
        name: 'Traffic',
        tooltip: {
            valueSuffix: '  Bits'
        }
    },
    {
        type: 'line',
        useHTML:'true',
        yAxis:2,
        data: [

        ],
        //fillColor:'#2f7ed8',
        name: 'Energy',
        tooltip: {
            valueSuffix: '  J'
        }
    }
    ]//end of series

});





}








function f1() {
  humidexchart[1].series[0].addPoint(
   [
        {y: Math.random()*100 , color:'red',marker:{symbol:"url(happy.png)"}},
        {y: Math.random()*100 , color:'red',marker:{symbol:"url(happy.png)"}}
    ]
    , true, true);
  callServer();
}


function callServer()
{
    var req = {
        'type': 'query',
        'time': 4500
    };
    ws.send(JSON.stringify(req));
}
function addPointToChart(chartNumber,seriesNumber, point)
{
    humidexchart[chartNumber].series[seriesNumber].addPoint(point);
}

globalcounter=0;
//somevar = [];
function updateDiagram(res)
{
    //console.log(res);
    //var comfort=res['timestamp'].zip(res['comfort'])
    //console.log(res);
   // somevar=res; 


    for (var i = res['timestamp'].length - 1; i >= 0; i--) {
            //comfort level with emojies
        humidexchart[1].series[0].addPoint(
            {
                x:res['timestamp'][i] +globalcounter,
                y:res['comfort'][i], color: "#00FF00"
                ,marker:{symbol:"url(emoji"+(6-comfort[i][1])+".png)"}
             }
        );

        //console.log('this is the size of the chart: '+humidexchart[1].series[0].length);


        //co2 emitted
        humidexchart[2].series[0].addPoint({
            x:res['timestamp'][i],
            y:res['co2'][i]
        } );

        //co2pbit
        humidexchart[2].series[1].addPoint({
            x:res['timestamp'][i],
            y:res['co2pbit'][i]
        } );

        //temperature
        humidexchart[3].series[0].addPoint({
            x:res['timestamp'][i],
            y:res['temperature'][i]
        } );
                //humidity
        humidexchart[3].series[1].addPoint({
            x:res['timestamp'][i],
            y:res['humidity'][i]
        } );
                //humidex
        humidexchart[3].series[2].addPoint({
            x:res['timestamp'][i],
            y:res['humidex'][i]
        } );
                //power
        humidexchart[4].series[0].addPoint({
            x:res['timestamp'][i],
            y:res['power'][i]
        } );
                //traffic
        humidexchart[4].series[1].addPoint({
            x:res['timestamp'][i],
            y:res['traffic'][i]
        });
                //energy
        // humidexchart[4].series[2].addPoint({
        //     x:res['timestamp'][i],
        //     y:res['energy'][i]
        // } );

        
    }
    humidexchart[1].redraw();
    humidexchart[2].redraw();
    humidexchart[3].redraw();
    humidexchart[4].redraw();


    // for (var i = comfort.length - 1; i >= 0; i--) {
    //         //console.log('x:'+comfort[i][0]+'y:'+comfort[i][1]);

    //     humidexchart[1].series[0].addPoint(
    //         {
    //             x:comfort[i][0]+globalcounter,
    //             y: comfort[i][1], color: "#00FF00"
    //         ,marker:{symbol:"url(emoji"+(6-comfort[i][1])+".png)"}
    //          },
    //     );

// }

        //co2 emitted

        // humidexchart[2].series[0].addPoint({
        //     x:
        //     y: 
        // } );

        
    
    globalcounter += 100;
}







// in the series...
    // {
    //     type: 'windbarb',
    //     data: 
    //     [
    //     ],
    //     name: 'Wind',
    //     color: Highcharts.getOptions().colors[1],
    //     showInLegend: false,
    //     tooltip: {
    //         valueSuffix: ' m/s'
    //     }
    // }, 

    // {
    //     type: 'scatter',
    //     keys: ['y', 'rotation'], // rotation is not used here
    //     data: 
    //     [],
    //     color: Highcharts.getOptions().colors[0],
    //     fillColor: {
    //         linearGradient: { x1: 0, x2: 0, y1: 0, y2: 1 },
    //         stops: [
    //             [0, Highcharts.getOptions().colors[0]],
    //             [
    //                 1,
    //                 Highcharts.color(Highcharts.getOptions().colors[0])
    //                     .setOpacity(0.25).get()
    //             ]
    //         ]
    //     },
    //     name: 'Comfort Level',
    //     tooltip: {
    //         //valueSuffix: ' m/s'
    //     }
    // },
