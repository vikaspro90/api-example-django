var appURL = "http://127.0.0.1:8000/";
var drchrono = angular .module("drchronoApp",[])
                        .controller("mainController", function($scope, $http){
                            // Get the local date in ISO format
                            var offset = (new Date()).getTimezoneOffset() * 60000;
                            var localISODate = (new Date(Date.now()-offset)).toISOString().slice(0, 10);
                            $scope.heading = "Please wait...";
                            $scope.patients=[];
                            $scope.messages={"emailMessage":"", "sendAllMessage":""};
                            $scope.handShake = function() {
                                /*
                                An initial handshake between the client and the server.
                                Sends the client date to the server and fetches current the doctor name.
                                 */
                                $http({
                                    method: "POST",
                                    url: appURL + "handShake/",
                                    data: {"clientDate": localISODate}
                                })
                                .then(function(response){
                                    $scope.docName = response.data.docName;
                                    updatePatientList();
                                },
                                function(response){
                                    // Could not reach server
                                    $scope.heading="Something went wrong while contacting the server. Please try after some time.";
                                });
                            };

                            function updatePatientList() {
                                /*
                                Gets the patients that were born on this day.
                                This is a callback called from handShake.
                                 */
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
                                },
                                function(response){
                                    // Could not reach server
                                    $scope.heading="Something went wrong while updating patient list.";
                                });
                            }

                            $scope.showDetails = function(p){
                                /*
                                Fetches the details of a particular patient.
                                Uses name and dob to uniquely identify patient.
                                 */
                                $scope.viewDetailsInfo = "Please wait while we retrieve the details..."
                                clearInfoMessages();
                                $scope.sendAllFlag=false;
                                $scope.sendingId="";
                                $http({
                                    method: "GET",
                                    url: appURL + "getPatientDetails/",
                                    params: {"fname": p.first_name,
                                    "lname": p.last_name,
                                    "dob": p.date_of_birth}
                                }).then(function(response){
                                    $scope.viewDetailsInfo = "";
                                    $scope.selectedId = p.id;
                                    $scope.currPatient = response.data.patient;
                                    $scope.buildEmail(p);
                                },
                                function(response){
                                    $scope.viewDetailsInfo = "Sorry. Failed to retrieve the details.";
                                });
                            };

                            $scope.cancelDetails = function(){
                                /*
                                Hides the patients details panel.
                                 */
                                $scope.selectedId = "";
                            };

                            $scope.quickSend = function(p){
                                /*
                                Displays a text box and send option to
                                quickly send a message to a patient.
                                 */
                                clearInfoMessages();
                                $scope.selectedId = "";
                                $scope.sendAllFlag=false;
                                $scope.sendingId = p.id;
                                $scope.buildEmail(p);
                            };

                            $scope.buildEmail = function(p){
                                /*
                                Builds an email to be sent to a particular patient.
                                If a patient does not have an email address on file, this
                                disables the text box and displays an appropriate message.
                                 */
                                if(p.email.length==0) {
                                    var textarea = document.getElementById("emailMessage"+p.id);
                                    textarea.setAttribute("readonly", "true");
                                    textarea = document.getElementById("emailMessageDet"+p.id);
                                    textarea.setAttribute("readonly", "true");
                                    $scope.messages.emailMessage = "Oops.. There is no emailId on file for "+p.first_name+" "+p.last_name+".";
                                    $scope.noEmailFlag = true;
                                    return;
                                }
                                $scope.noEmailFlag = false;
                                $scope.messages.emailMessage = "Hello "+p.first_name+" "+p.last_name+", " +
                                    "\n\nWish you a wonderful birthday and great health.\n\n..from Dr."+$scope.docName;
                            };

                            $scope.cancelSend = function(){
                                /*
                                Hides the quick send panel.
                                 */
                                clearInfoMessages();
                                $scope.sendingId="";
                            };

                            $scope.showSendAll = function(){
                                /*
                                Displays the text box and send option to send a
                                message to all those who have birthdays today.
                                 */
                                $scope.sendAllFlag=true;
                                $scope.selectedId="";
                                $scope.sendingId="";
                                clearInfoMessages();
                                $scope.messages.sendAllMessage = "Wish you a wonderful birthday and great health.\n\n..from Dr."+$scope.docName;
                            };

                            $scope.cancelSendAll = function(){
                                /*
                                Hides the send all panel.
                                 */
                                clearInfoMessages();
                                $scope.sendAllFlag=false;
                            };

                            $scope.sendAll = function(){
                                /*
                                Builds the list of email addresses and calls the sendEmail() function to send emails.
                                 */
                                $scope.sendAllInfo = "Sending..";
                                var emails = [];
                                var names = [];
                                var noEmail = [];
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
                                /*
                                Sends a single email or multiple emails based on the
                                arguments received and configures the message displayed
                                to the user accordingly.
                                 */
                                $scope.sendOneInfo = "Sending...";
                                disableButtons();
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
                                    enableButtons();
                                },
                                function(response){
                                    // Could not reach server
                                    $scope.sendOneInfo="Something went wrong while sending email.";
                                    $scope.sendAllInfo="Something went wrong while sending email(s).";
                                    enableButtons();
                                });
                            };

                            function clearInfoMessages(){
                                /*
                                Reset the messages displayed to the user.
                                 */
                                $scope.sendOneInfo="";
                                $scope.sendAllInfo="";
                                $scope.viewDetailsInfo="";
                            }

                            function enableButtons(){
                                /*
                                Enables the send and cancel buttons below the text area.
                                Called when a response is received from the server after clicking
                                on send.
                                 */
                                var sends = document.getElementsByClassName("emailSend");
                                var cancels = document.getElementsByClassName("emailCancel");
                                for(var i=0; i<cancels.length; i++){
                                    sends[i].removeAttribute("disabled");
                                    cancels[i].removeAttribute("disabled");
                                }
                            }

                            function disableButtons(){
                                /*
                                Disables the send and cancel buttons below the text area.
                                Called when send is clicked.
                                 */
                                var sends = document.getElementsByClassName("emailSend");
                                var cancels = document.getElementsByClassName("emailCancel");
                                for(var i=0; i<cancels.length; i++){
                                    sends[i].setAttribute("disabled", "");
                                    cancels[i].setAttribute("disabled", "");
                                }
                            }
                        })

					.config(function ($httpProvider) {
                        // Needed for enabling cookies
						$httpProvider.defaults.withCredentials = true;
                        // Needed for proper handling of the django csrftoken
                        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
                        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
					});