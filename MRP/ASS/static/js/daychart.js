var date = datet.reverse();
var open = opent.reverse();
var close = closet.reverse();
var high = hight.reverse();
var low = lowt.reverse();
var volumes = volumest.reverse();
var dataMA5 = dataMA5t.reverse();
var dataMA10 = dataMA10t.reverse();
var dataMA20 = dataMA20t.reverse();

var data ={
    open_price: open,
    close_price: close
}

var colorList = ['#c23531','#2f4554', '#61a0a8', '#d48265', '#91c7ae','#749f83',  '#ca8622', '#bda29a','#6e7074', '#546570', '#c4ccd3'];
var labelFont = 'bold 12px Sans-serif';

function calculateMA(dayCount, data) {
    var result = [];
    for (var i=0,len = data.length; i < len; i++) {
        if (i < dayCount) {
            result.push('-');
            continue;
        }
        var sum = 0;
        for (var j = 0; j < dayCount; j++) {
            sum += data[i - j];
        }
        result.push((sum / dayCount).toFixed(2));
    }
    return result;
}
var data = [[]];
for (var i = open.length; i>=0;i--){
    var datatemp =[0,0,0,0,0];
    datatemp[0] = open[i];
    datatemp[1] = close[i];
    datatemp[2] = low[i];
    datatemp[3] = high[i];
    datatemp[4] = volumes[i];
    data.push(datatemp);
}
var data1 = data.reverse();
var option = {
    animation: true,
    color: colorList,
    legend: {
        top: 20,
        data: ['日K', 'MA5', 'MA10', 'MA20']
    },
    tooltip: {
        triggerOn: 'none',
        transitionDuration: 0,
        confine: true,
        bordeRadius: 4,
        borderWidth: 1,
        borderColor: '#333',
        backgroundColor: 'rgba(255,255,255,0.9)',
        textStyle: {
            fontSize: 12,
            color: '#333'
        },
        position: function (pos, params, el, elRect, size) {
            var obj = {
                top: 60
            };
            obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 5;
            return obj;
        }
    },
    axisPointer: {
        link: [{
            xAxisIndex: [0, 1]
        }]
    },
    dataZoom: [{
        type: 'slider',
        xAxisIndex: [0, 1],
        realtime: false,
        start: date.length < 60 ? 0:100-parseInt(6000/date.length),
        end: 100,
        top: 65,
        height: 20,
        handleIcon: 'M10.7,11.9H9.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4h1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
        handleSize: '120%'
    }, {
        type: 'inside',
        xAxisIndex: [0, 1],
        start: 40,
        end: 70,
        top: 30,
        height: 20
    }],
    xAxis: [{
        type: 'category',
        data: date,
        boundaryGap : false,
        axisLine: { lineStyle: { color: '#777' } },
        axisLabel: {
            formatter: function (value) {
                return echarts.format.formatTime('MM-dd', value);
            }
        },
        min: 'dataMin',
        max: 'dataMax',
        axisPointer: {
            show: true
        }
    }, {
        type: 'category',
        gridIndex: 1,
        data: date,
        scale: true,
        boundaryGap : false,
        splitLine: {show: false},
        axisLabel: {show: false},
        axisTick: {show: false},
        axisLine: { lineStyle: { color: '#777' } },
        splitNumber: 20,
        min: 'dataMin',
        max: 'dataMax',
        axisPointer: {
            type: 'shadow',
            label: {show: false},
            triggerTooltip: true,
            handle: {
                show: true,
                margin: 30,
                color: '#B80C00'
            }
        }
    }],
    yAxis: [{
        scale: true,
        splitNumber: 2,
        axisLine: { lineStyle: { color: '#777' } },
        splitLine: { show: true },
        axisTick: { show: false },
        axisLabel: {
            inside: true,
            formatter: '{value}\n'
        }
    }, {
        scale: true,
        gridIndex: 1,
        splitNumber: 2,
        axisLabel: {show: false},
        axisLine: {show: false},
        axisTick: {show: false},
        splitLine: {show: false}
    }],
    grid: [{
        left: 25,
        right: 25,
        top: 110,
        height: 300
    }, {
        left: 25,
        right: 25,
        height: 100,
        top: 440
    }],
    graphic: [{
        type: 'group',
        left: 'center',
        top: 70,
        width: 300,
        bounding: 'raw',
        children: [{
            id: 'MA5',
            type: 'text',
            style: {fill: colorList[1], font: labelFont},
            left: 0
        }, {
            id: 'MA10',
            type: 'text',
            style: {fill: colorList[2], font: labelFont},
            left: 'center'
        }, {
            id: 'MA20',
            type: 'text',
            style: {fill: colorList[3], font: labelFont},
            right: 0
        }]
    }],
    series: [{
        name: 'Volume',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        itemStyle: {
            normal: {
                color: '#7fbe9e'
            },
            emphasis: {
                color: '#140'
            }
        },
        data: volumes
    }, {
        type: 'candlestick',
        name: '日K',
        data: data,
        itemStyle: {
            normal: {
                color: '#ef232a',
                color0: '#14b143',
                borderColor: '#ef232a',
                borderColor0: '#14b143'
            },
            emphasis: {
                color: 'black',
                color0: '#444',
                borderColor: 'black',
                borderColor0: '#444'
            }
        }
    }, {
        name: 'MA5',
        type: 'line',
        data: dataMA5,
        smooth: true,
        showSymbol: false,
        lineStyle: {
            normal: {
                width: 1
            }
        }
    }, {
        name: 'MA10',
        type: 'line',
        data: dataMA10,
        smooth: true,
        showSymbol: false,
        lineStyle: {
            normal: {
                width: 1
            }
        }
    }, {
        name: 'MA20',
        type: 'line',
        data: dataMA20,
        smooth: true,
        showSymbol: false,
        lineStyle: {
            normal: {
                width: 1
            }
        }
    }]
};
myChart.setOption(option);
window.onresize = function () {
    myChart.resize();
}
