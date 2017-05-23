var appURL = "http://127.0.0.1:8000/";
var drchrono = angular .module("drchronoApp",[])
                        .controller("mainController", function($scope, $http){
                            // Get the local date in ISO format
                            var offset = (new Date()).getTimezoneOffset() * 60000;
                            var localISODate = (new Date(Date.now()-offset)).toISOString().slice(0, 10);
                            $scope.heading = "Please wait...";
                            $scope.patients=[];
                            $scope.emailMessage = "";
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
                                    $scope.heading="Something went wrong while contacting the server.";
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
                                    $scope.heading="Something went wrong while updating patient list.";
                                });
                            }

                            $scope.sendWishes = function sendWishes(p){
                                $scope.selectedId = p.id;
                                if(p.email.length==0) {
                                    var textarea = document.getElementById("emailMessage"+p.id);
                                    textarea.setAttribute("readonly", "true");
                                    $scope.emailMessage = "Oops.. There is no emailId on file for "+p.first_name+" "+p.last_name+".";
                                    $scope.noEmail = true;
                                    return;
                                }
                                $scope.noEmail = false;
                                console.log($scope.selectedId +" "+ p.id);
                                $scope.emailMessage = "Dear "+p.first_name+" "+p.last_name+", \n\nMany many happy returns of the day.\n\n..from your caring doctor.";
                                console.log($scope.emailMessage);
                            };

                            $scope.sendEmail = function(email){
                                var emails = [email];
                                $http({
                                    method: "POST",
                                    url: appURL + "sendEmail/",
                                    data: {"toList": emails, "message": $scope.emailMessage}
                                })
                                .then(function(response){
                                    // Success
                                    console.log("Sent email");
                                },
                                function(response){
                                    // Could not reach server
                                    $scope.heading="Something went wrong while sending email(s).";
                                });
                            };

                            $scope.cancelSend = function(){
                                $scope.selectedId="";
                            }
                        })

					.config(function ($httpProvider) {
						$httpProvider.defaults.withCredentials = true;
                        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
                        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
					});