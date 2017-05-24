var appURL = "http://127.0.0.1:8000/";
var drchrono = angular .module("drchronoApp",[])
                        .controller("mainController", function($scope, $http){
                            // Get the local date in ISO format
                            var offset = (new Date()).getTimezoneOffset() * 60000;
                            var localISODate = (new Date(Date.now()-offset)).toISOString().slice(0, 10);
                            console.log(localISODate);
                            $scope.heading = "Please wait...";
                            $scope.patients=[];
                            $scope.messages={"emailMessage":"", "sendAllMessage":""};
                            $scope.handShake = function() {
                                console.log($scope.docName);
                                console.log(localISODate);
                                $http({
                                    method: "POST",
                                    url: appURL + "handShake/",
                                    data: {"clientDate": localISODate}
                                })
                                .then(function(response){
                                    $scope.docName = response.data.docName;
                                    console.log(response);
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

                            $scope.showDetails = function(p){
                                clearSendMessages();
                                $scope.sendAllFlag=false;
                                $scope.sendingId="";
                                $http({
                                    method: "GET",
                                    url: appURL + "getPatientDetails/",
                                    params: {"fname": p.first_name,
                                    "lname": p.last_name,
                                    "dob": p.date_of_birth}
                                }).then(function(response){
                                    console.log(response.data.patient);
                                    $scope.selectedId = p.id;
                                    $scope.currPatient = response.data.patient;
                                },
                                function(response){

                                });
                            };

                            $scope.cancelDetails = function(){
                                $scope.selectedId = "";
                            };

                            $scope.sendWishes = function(p){
                                clearSendMessages();
                                $scope.selectedId = "";
                                $scope.sendAllFlag=false;
                                $scope.sendingId = p.id;
                                if(p.email.length==0) {
                                    var textarea = document.getElementById("emailMessage"+p.id);
                                    textarea.setAttribute("readonly", "true");
                                    $scope.messages.emailMessage = "Oops.. There is no emailId on file for "+p.first_name+" "+p.last_name+".";
                                    $scope.noEmail = true;
                                    return;
                                }
                                $scope.noEmail = false;
                                console.log($scope.sendingId +" "+ p.id);
                                $scope.messages.emailMessage = "Hello "+p.first_name+" "+p.last_name+", " +
                                    "\n\nWish you a wonderful birthday and great health.\n\n..from Dr."+$scope.docName;
                                console.log($scope.messages.emailMessage);
                            };

                            $scope.cancelSend = function(){
                                clearSendMessages();
                                $scope.sendingId="";
                            };

                            $scope.showSendAll = function(){
                                $scope.sendAllFlag=true;
                                $scope.selectedId="";
                                $scope.sendingId="";
                                clearSendMessages();
                                $scope.messages.sendAllMessage = "Wish you a wonderful birthday and great health.\n\n..from Dr."+$scope.docName;
                            };

                            $scope.cancelSendAll = function(){
                                clearSendMessages();
                                $scope.sendAllFlag=false;
                            };

                            $scope.sendAll = function(){
                                $scope.sendAllInfo = "Sending..";
                                var emails = [];
                                var names = [];
                                var noEmail = [];
                                console.log($scope.patients);
                                $scope.patients.forEach(function(p){
                                    if (p.email == "") {
                                        noEmail.push(p.first_name + " " + p.last_name);
                                    }
                                    else {
                                        emails.push(p.email);
                                        names.push(p.first_name+" "+p.last_name);
                                    }
                                });
                                $scope.messages.emailMessage = $scope.messages.sendAllMessage;
                                $scope.sendEmail(emails, names);
                            };

                            $scope.sendEmail = function(email, names){
                                var mode="multiple";
                                if(typeof email === "string") {
                                    var email = [email];
                                    mode="single";
                                }
                                $http({
                                    method: "POST",
                                    url: appURL + "sendEmail/",
                                    data: {"toList": email, "message": $scope.messages.emailMessage, "mode": mode, "names":names}
                                })
                                .then(function(response){
                                    // Success
                                    if(mode=="multiple"){
                                        var numSent = email.length;
                                        var numNoEmail = $scope.patients.length-numSent;
                                        var noEmailMsg = "No email found for "+numNoEmail+" patient(s).";
                                        if(numNoEmail==0) noEmailMsg="";
                                        $scope.sendAllInfo = "Email sent to "+numSent+" patient(s). "+noEmailMsg;
                                    }
                                    else{
                                        $scope.sendOneInfo = "Email sent.";
                                    }
                                    console.log("Sent email");
                                },
                                function(response){
                                    // Could not reach server
                                    $scope.sendOneInfo="Something went wrong while sending email.";
                                    $scope.sendAllInfo="Something went wrong while sending email(s).";
                                });
                            };

                            function clearSendMessages(){
                                $scope.sendOneInfo="";
                                $scope.sendAllInfo="";
                            }
                        })

					.config(function ($httpProvider) {
						$httpProvider.defaults.withCredentials = true;
                        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
                        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
					});