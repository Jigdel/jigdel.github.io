var ourHydro = angular.module('ourHydro', []);

ourHydro.service("postalCodeService", function postalCodeService($http, $q){

	this.getMPPs = function(newPostalCode) {

		var deferred = $q.defer();
		console.log('New postal code: ', newPostalCode);

		httpPromise = $http.get('client/data/data.json');

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

		httpSecondPromise = $http.get('client/data/mppSocial.json');
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

ourHydro.controller('MainCtrl', [function() {
		var self = this;
		self.tab = 'infographic';
		self.open = function(tab) {
			self.tab = tab;
		};
}]);

ourHydro.controller('SubCtrl', [function SubCtrl () {
		var self = this;
		self.list = [
			{id: 1, label: 'Item 0'},
			{id: 2, label: 'Item 1'}
		];

		self.add = function() {
			self.list.push({
				id: self.list.length + 1,
				label: 'Item ' + self.list.length
			});
		};	
}]);