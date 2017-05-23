var appURL = "http://127.0.0.1:8000/";
var drchrono = angular .module("drchronoApp",[])
                        .controller("mainController", function($scope, $http){
                            // Get the local date in ISO format
                            var offset = (new Date()).getTimezoneOffset() * 60000;
                            var localISODate = (new Date(Date.now()-offset)).toISOString().slice(0, 10);
                            $scope.heading = "Please wait...";
                            $scope.updateClientDate = function() {
                                $http({
                                    method: "POST",
                                    url: appURL + "updateClientDate/",
                                    data: {"clientDate": localISODate}
                                })
                                .then(function(response){
                                    updatePatientList();
                                },
                                function(response){
                                    // Could not reach server
                                    $scope.heading="Something went wrong in updating client time";
                                });
                            };

                            function updatePatientList() {
                                $http({
                                    method: "GET",
                                    url: appURL + "updatePatientList/"
                                })
                                .then(function(response){
                                    // Success
                                    $scope.patients=response.data.patients;
                                    if($scope.patients.length==0){
                                        $scope.heading="None of your patients were born on this day.";
                                    }
                                    else{
                                        $scope.heading="Below are your patients that were born on this day.";
                                    }
                                    // console.log(response)
                                },
                                function(response){
                                    // Could not reach server
                                    $scope.heading="Something went wrong in updating patient list";
                                });
                            }
                        })

					.config(function ($httpProvider) {
						$httpProvider.defaults.withCredentials = true;
                        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
                        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
					});