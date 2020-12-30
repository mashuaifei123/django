//var rew_date = rew_datet.reverse();
//var rew_wd = rew_wdt.reverse();
//var res_sd = res_sdt.reverse();
var rew_date = rew_datet;
var rew_wd = rew_wdt;
var res_sd = res_sdt;
var wd_box = wd_boxt;
var sd_box = sd_boxt;
var wsd_box = wsd_boxt;
var series=[];

for(var i = 0;i< wd_box.length;i++){
    series.push(
        {
            name: wd_box[i],
            type: 'line',
            symbolSize: 8,
            hoverAnimation: false,
//            symbol: 'circle',
//            itemStyle: {
//            color: "#6f7de3",
//            },
            data: rew_wd[i]
        },
        {
            name: sd_box[i],
            type: 'line',
            xAxisIndex: 1,
            yAxisIndex: 1,
            symbolSize: 8,
//            symbol: 'circle',
//            itemStyle: {
//            color: "#c257F6",
//            },
            hoverAnimation: false,
            data: res_sd[i]
         }
    )
}


var timeData = rew_date;
timeData = timeData.map(function (str) {
    return str.replace('2017/', '');
});

option = {
    title: {
        text: '温度湿度关系图',
        subtext: '数据来数据库',
        left: 'center'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            animation: false
        }
    },


    toolbox: {
        feature: {
            dataZoom: {
                yAxisIndex: 'none'
            },
            restore: {},
            saveAsImage: {}
        }
    },
    axisPointer: {
        link: {xAxisIndex: 'all'}
    },
    dataZoom: [
        {
            show: true,
            realtime: true,
            start: 30,
            end: 70,
            xAxisIndex: [0, 1]
        },
        {
            type: 'inside',
            realtime: true,
            start: 30,
            end: 70,
            xAxisIndex: [0, 1]
        }
    ],
    grid: [{
        left: 50,
        right: 50,
        top: '13%',
        height: '33%'
    }, {
        left: 50,
        right: 50,
        top: '55%',
        height: '33%'
    }],

    xAxis: [
        {
            type: 'category',
            boundaryGap: false,
            axisLine: {onZero: true},
            data: timeData
        },
        {
            gridIndex: 1,
            type: 'category',
            boundaryGap: false,
            axisLine: {onZero: true},
            data: timeData,
            position: 'bottom'
        }
    ],
    yAxis: [
        {
            name: '温度(℃)',
            type: 'value',
            scale: true,
            max: 26,
            min: 10
        },
        {
            gridIndex: 1,
            name: '湿度(RH%)',
            type: 'value',
            inverse: false,
            scale: true,
            min: 30,
            max: 80
        }
    ],

    legend: {
        data: wsd_box,
        left: 10
    },
    series:series

};
myChart.setOption(option);
window.onresize = function () {
    myChart.resize();
}
