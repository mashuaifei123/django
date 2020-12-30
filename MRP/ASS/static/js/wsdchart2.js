var timeData = date1t;
var wd = wdt;
var mr = wd_mrt;



var mr_bar = wd_mr_bart;
var cl1 = wd_ucl_ct;
var cl2 = wd_ucl_bt;
var cl3 = wd_lcl_ct;
var cl4 = wd_lcl_bt;
var lcl = wd_uclt;
var ucl = wd_lclt;

var wd_bar = wd_bart;
var mr_cl1 = wd_mr_ucl_ct ;
var mr_cl2 = wd_mr_ucl_bt ;
var mr_cl3 = wd_mr_lcl_ct ;
var mr_cl4 = wd_mr_lcl_bt ;
var mr_lcl = wd_mr_lclt;
var mr_ucl = wd_mr_uclt;

var wd_max = wd_maxt
var wd_min = wd_mint
var mr_max = mr_maxt


option = {
    title: [{
            text: 'I Chart',
            left: 'center'
        },
        {
            text: 'MR Chart',
            left: "center",
            top: "center",
        },


    ],
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            animation: false
        }
    },
    legend: [{
            data: ['X_BAR', 'CL'],
            left: 10,
            type: 'scroll',
            orient: 'vertical',
        },
        {
            data: ['MR'],
            left: 10,
            top: 300,
            type: 'scroll',
            orient: 'vertical',
        }

    ],
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
        link: {
            xAxisIndex: ''
        }
    },

    grid: [{
        left: 70,
        right: 70,
        height: '30%',
        top: '8%',
    }, {
        left: 70,
        right: 70,
        top: '60%',
        height: '30%'
    }],
    xAxis: [{
            type: 'category',
            boundaryGap: false,
            axisLine: {
                onZero: true
            },
            data: timeData
        },
        {
            gridIndex: 1,
            type: 'category',
            boundaryGap: false,
            axisLine: {
                onZero: true
            },
            data: timeData,
            position: ''
        }
    ],
    yAxis: [{
            type: 'value',
            scale: true,
            min: wd_min,
            max: wd_max

        },
        {
            gridIndex: 1,
            type: 'value',
            inverse: false,
            scale: true,
            min: 0,
            max: mr_max
        }
    ],
    series: [{
            name: 'X_BAR',
            type: 'line',
            symbol: 'circle',
            symbolSize: 6,
            hoverAnimation: false,
            itemStyle: {
                color: 'black'
            },
            lineStyle: {
                color: 'black'
            },

            markLine: {
                silent: true,
                symbol: ['none', 'none'],
                itemStyle: {
                    normal: {
                        lineStyle: {},
                        label: {
                            show: false,
                            position: 'end'
                        }
                    }
                },
                data: [{
                    lineStyle: {
                        color: "#6c50f3"
                    },
                    yAxis: cl1,

                }, {
                    lineStyle: {
                        color: "#6c50f3"
                    },
                    yAxis: cl2
                }, {
                    lineStyle: {
                        color: "#6c50f3"
                    },
                    yAxis: cl3
                }, {
                    lineStyle: {
                        color: "#6c50f3"
                    },
                    yAxis: cl4
                }, {
                    label: {
                        show: true,
                        formatter: 'LCL'
                    },
                    lineStyle: {
                        color: "#6c50f3",
                        type: 'solid',
                        width: 1.2
                    },
                    yAxis: ucl
                }, {
                    label: {
                        show: true,
                        formatter: 'UCL'
                    },
                    lineStyle: {
                        color: "#6c50f3",
                        type: 'solid',
                        width: 1.2
                    },
                    yAxis: lcl
                }, {
                    lineStyle: {
                        type: 'solid',
                        width: 1.3,
                        color: 'red'
                    },
                    name: 'CL',
                    label: {
                        show: true,
                        formatter: 'CL'
                    },
                    yAxis: wd_bar,
                }]
            },
            data:wd,
        },
        {
            name: 'MR',
            type: 'line',
            xAxisIndex: 1,
            yAxisIndex: 1,
            symbol: 'circle',
            symbolSize: 6,
            itemStyle: {
                color: 'black'
            },
            lineStyle: {
                color: 'black'
            },
            hoverAnimation: false,
            data: mr,
            markLine: {
                silent: true,
                symbol: ['none', 'none'],
                itemStyle: {
                    normal: {
                        lineStyle: {},
                        label: {
                            show: false,
                            position: 'end'
                        }
                    }
                },
                data: [{
                    lineStyle: {
                        color: "#6c50f3"
                    },
                    yAxis: mr_cl1,

                }, {
                    lineStyle: {
                        color: "#6c50f3"
                    },
                    yAxis: mr_cl2
                }, {
                    lineStyle: {
                        color: "#6c50f3"
                    },
                    yAxis: mr_cl3
                }, {
                    lineStyle: {
                        color: "#6c50f3"
                    },
                    yAxis: mr_cl4
                }, {
                    label: {
                        show: true,
                        formatter: 'LCL'
                    },
                    lineStyle: {
                        color: "#6c50f3",
                        type: 'solid',
                        width: 1.2
                    },
                    yAxis: 0
                }, {
                    label: {
                        show: true,
                        formatter: 'UCL'
                    },
                    lineStyle: {
                        color: "#6c50f3",
                        type: 'solid',
                        width: 1.2
                    },
                    yAxis: mr_ucl
                }, {
                    lineStyle: {
                        type: 'solid',
                        width: 1.3,
                        color: 'red'
                    },
                    name: 'CL',
                    label: {
                        show: true,
                        formatter: 'CL',
                        color: 'red'
                    },
                    yAxis: mr_bar,
                    color: '',
                }]
            },
        }
    ]
};

myChart.setOption(option);
window.onresize = function () {
    myChart.resize();
}