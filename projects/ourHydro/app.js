var myApp = angular.module('myApp', []);

function MyCtrl($scope, limitToFilter) {
  $scope.ideas = [
    ['ideas1', 1],
    ['ideas2', 8],
    ['ideas3', 5]
  ];
  
  $scope.limitedIdeas = limitToFilter($scope.ideas, 2);
}



 myApp.directive('hcPie', function () {
  return {
    restrict: 'C',
    replace: true,
    scope: {
      items: '='
    },
    controller: function ($scope, $element, $attrs) {
      console.log(2);

    },
    link: function (scope, element, attrs) {
        
      var chart = new Highcharts.Chart({
        chart: {
          renderTo: $(element).attr('id'),
          plotBackgroundColor: null,
          plotBorderWidth: null,
          plotShadow: false
        },
        title: {
          text: 'Browser market shares at a specific website, 2010'
        },
        tooltip: {
          pointFormat: '{series.name}: <b>{point.percentage}%</b>',
          percentageDecimals: 1
        },
        plotOptions: {
          pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
              enabled: true,
              color: '#000000',
              connectorColor: '#000000',
              formatter: function () {
                return '<b>' + this.point.name + '</b>: ' + this.percentage + ' %';
              }
            }
          }
        },
        series: [{
          type: 'pie',
          name: 'Browser share',
          data: scope.items
        }]
      });
      scope.$watch("items", function (newValue) {
        chart.series[0].setData(newValue, true);
      }, true);
      
    }
  }
});