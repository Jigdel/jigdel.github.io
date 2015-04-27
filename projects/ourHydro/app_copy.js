'use strict';

var myapp = angular.module('myapp', ["highcharts-ng"]);


myapp.controller('chartsCtrl', function ($scope) {

/*
    $scope.addPoints = function () {
        var seriesArray = $scope.highchartsNG.series
        var rndIdx = Math.floor(Math.random() * seriesArray.length);
        seriesArray[rndIdx].data = seriesArray[rndIdx].data.concat([1, 10, 20])
    };
*/

    $scope.hydroIncome = function () {
        /*
        var incomeData = [.455,.399,.498,.470,.591,.641,.745,.803,.749];
        var chartTitle = 'Income and dividends';

        $scope.highchartsNG.series.push({
            name: 'Income & Dividends',
            data: incomeData
        });
        $scope.highchartsNG.title({
            text: chartTitle
        })
        */
        $scope.highchartsNG = {
        options: {
            chart: {
                type: 'column'
            }
        },
        title: {
            text: 'Annual Net Income and Dividends'  
        },
        xAxis: {
            categories: [2006,2007,2008,2009,2010,2011,2012,2013,2014]
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Billions($)'
            }
        },
        tooltip: {
            formatter: function () {
                return this.series.name + ': $' + this.y + 'M' + '<br/>' +
                    'Total: ' + this.point.stackTotal;
            }
        },
        plotOptions: {
            column: {
                stacking: 'percent',
                dataLabels: {
                    enabled: true,
                    color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
                    style: {
                        textShadow: '0 0 3px black'
                    }
                }
            }
        },
        series: [{
            name: 'Dividends',
            data: [350,325,259,188,28,168,370,218,287]
        }, {
            name: 'Net Income',
            data: [455,399,498,470,591,641,745,803,749]
        }],
        credits: {
            enabled: false
        },
        loading: false
        }
    };


    $scope.removeRandomSeries = function () {
        var seriesArray = $scope.highchartsNG.series
        var rndIdx = Math.floor(Math.random() * seriesArray.length);
        seriesArray.splice(rndIdx, 1)
    }

    $scope.options = {
        type: 'line'
    }

    $scope.swapChartType = function () {
        if (this.highchartsNG.options.chart.type === 'line') {
            this.highchartsNG.options.chart.type = 'column'
        } else {
            this.highchartsNG.options.chart.type = 'line'
        }
    }


    $scope.highchartsNG = {
        options: {
            chart: {
                type: 'column'
            }
        },
        series: [{
            name: 'Revenue',
            data: [4.545,4.655,4.597,4.744,5.124,5.471,5.728,6.074,6.548]
        }],
        title: {
            text: 'Annual Revenues'
        },
        xAxis: {
            categories: [2006,2007,2008,2009,2010,2011,2012,2013,2014]
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Billions($)'
            },
            stackLabels: {
                enabled: true,
                style: {
                    fontWeight: 'bold',
                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                }
            }
        },
        legend: {
            align: 'right',
            x: -30,
            verticalAlign: 'top',
            y: 25,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
            borderColor: '#CCC',
            borderWidth: 1,
            shadow: false
        },
        credits: {
            enabled: false
    },
        loading: false
    }

});
/*
xAxis: {
            categories: [
                'Jan',
                'Feb',
                'Mar',
                'Apr',
                'May',
                'Jun',
                'Jul',
                'Aug',
                'Sep',
                'Oct',
                'Nov',
                'Dec'
            ],

*/