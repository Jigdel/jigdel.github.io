'use strict';

var ourHydro = angular.module('ourHydro', ["highcharts-ng"]);

ourHydro.service("postalCodeService", function postalCodeService($http, $q){

	this.getMPPs = function(newPostalCode) {

		var deferred = $q.defer();
		console.log('New postal code: ', newPostalCode);

		var httpPromise = $http.get('client/data/data.json');

		// M1T3W6
		// https://represent.opennorth.ca/postcodes/M1T3L5/?sets=ontario-electoral-districts
		//httpPromise = $http.get('https://represent.opennorth.ca/postcodes/'+newPostalCode+'/?sets=ontario-electoral-districts');
		httpPromise.then(function (response) {
			deferred.resolve(response);
		});
		return deferred.promise;
	};

	this.getSocialMPPs = function() {
		var deferredSecond = $q.defer();
		//console.log('MPP name: ', mppName);

		var httpSecondPromise = $http.get('client/data/mppSocial.json');
		httpSecondPromise.then(function (response) {
			deferredSecond.resolve(response);
		});
		return deferredSecond.promise;
	};
	
});

ourHydro.controller("MppCtrl", function MppCtrl($scope, postalCodeService) {

	var self = this;
	$scope.submit = function(newPostalCode){
		//console.log('User clicked submit: ', newPostalCode);
		var promise = postalCodeService.getMPPs(newPostalCode);
		promise.then(function (response) {
			$scope.mpp = response.data;
			//console.log('Social data: ', $scope.mpp.representatives_concordance[0].name);
			$scope.mppName = $scope.mpp.representatives_concordance[0].name;
			var secondPromise = postalCodeService.getSocialMPPs();
			
			$scope.mppSocialAccount = [];
			secondPromise.then(function (response) {
				$scope.mppSocial = response.data;
				for (var i = 0; i < $scope.mppSocial.length; i++) {
					if ($scope.mppSocial[i].Name == $scope.mppName) {
						//$scope.mppSocialAccout['Twitter'] = $scope.mppSocial[i].
						//console.log($scope.mppSocial[i].Twitter);
						$scope.mppSocialAccount.push($scope.mppSocial[i].Twitter);
						$scope.mppSocialAccount.push($scope.mppSocial[i].Facebook);
						break;
					};
				};
				console.log('Social data: ', $scope.mppSocialAccount);
			})
			//console.log($scope.mpp);
			
		});
	}
});

// HighCharts
ourHydro.controller('chartsCtrl', function ($scope) {

    $scope.hydroIncome = function () {
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
                text: 'Millions($)'
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
                stacking: 'normal',
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

	$scope.hydroRevenue = function () {
        $scope.highchartsNG = {options: {
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
};

$scope.hydroDistCust = function () {
        $scope.highchartsNG = {
        options: {
            chart: {
                type: 'column'
            }
        },
        series: [{
            name: 'Distribution Customers',
            data: [1.293396,1.311714,1.325745,1.333920,1.345177,1.365379,1.381926,1.390000,1.400000]
        }],
        title: {
            text: 'Distribution Customers'
        },
        xAxis: {
            categories: [2006,2007,2008,2009,2010,2011,2012,2013,2014]
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Number of customers (Million)'
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
};
    $scope.hydroAssets = function () {
        $scope.highchartsNG = {
        options: {
            chart: {
                type: 'column'
            }
        },
        title: {
            text: 'Asset Breakdown'  
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
                stacking: 'normal',
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
            name: 'Other Assets',
            data: [.099,.106,.128,.161,.609,.652,.604,.974]
        }, {
            name: 'Transmission Assets',
            data: [6.950,7.273,7.877,8.993,9.805,10.380,11.586,11.586]
        }, {
            name: 'Distribution Assets',
            data: [5.161,5.407,5.873,6.481,6.908,7.336,8.621,8.805]
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