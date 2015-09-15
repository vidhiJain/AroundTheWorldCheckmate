function register(form){
	$.ajax({
	type: 'POST',
	data: form.serialize(),
	url: server_ip+'api/register/',
	success: function(response){
		switch(response){
			case 'success':
				user = $('#reg_form input[name="username"]').val();
				user64=window.btoa(user+':'+$('#reg_form input[name="password"]').val());
				login_start();
				break;
			case 'username_taken':
				my_alert("This Username is already taken!")
				break;
			case 'reg_closed':
				my_alert("Registration is closed currently")
				break;
			default:
				my_alert('Some Error Occured: ' + response);
		}
	}
	});
}
function check_user(){
	$.ajax({
	type: 'GET',
	url: server_ip+'api/check_user/',
	headers: {'Authorization': "Basic " + user64},
	statusCode: {
	      401: function (response) {
			my_alert("Username or Password incorrect");
			return;
	      },
	      403: function (response) {
			my_alert("You were not allowed to login due to some reason.");
			return;
	      }
	   },
	success: function(response){
		login_start();
	}
	});
}
function user_status(){
	$.ajax({
	type: 'GET',
	url: server_ip+'api/user_status/',
	headers: {'Authorization': "Basic " + user64},
	success: function(response){
		set_score(response["score"]);
		$('#currLoc,#loc_info').html(response["curr_loc"]);
		var time = parseInt(response["stay_duration"]);
		start_stopwatch(parseInt(time/60),parseInt(time%60));
		if(response["question"]=="")
		{
			$('#ques_cont .nano-content').html('No question for this location.');
			$('#ans_cont').css('display','none');
			$('.info').css('display','none');
		}
		else
		{
			$('#ans_cont').css('display','');
			$('.info').css('display','');
			if(response["attempts_left"]==-1)
			{
				$('#attempt_left').html('Solved');
				$('#ans_cont').css('display','none');
			}
			else
				$('#attempt_left').html(response["attempts_left"]);
			if(response["attempts_left"]==0)
			{
				$('#ans_cont').css('display','none');
			}
			$('#ques_cont .nano-content').html(response["question"]);
		}
	}
	});
}
function exit_game(){
	$.ajax({
	type: 'POST',
	url: server_ip+'api/exit_game/',
	headers: {'Authorization': "Basic " + user64},
	success: function(response){
		console.log(response);
	}
	});
}
function lboard(){
	$.ajax({
	type: 'GET',
	url: server_ip+'api/lboard/',
	success: function(response){
		console.log(response);
	}
	});
}
function site_status(){
	$.ajax({
	type: 'GET',
	url: server_ip+'api/site_status/',
	success: function(response){
		console.log(response);
	}
	});
}
function fly_to(destination){
	$.ajax({
	type: 'POST',
	data: destination,
	url: server_ip+'api/fly_to/',
	headers: {'Authorization': "Basic " + user64},
	success: function(response){
		if(response.hasOwnProperty('question')){
			set_score(response["score"]);
			if(response["question"]=="")
			{
				$('#ans_cont').css('display','none');
				$('#ques_cont .nano-content').html('No question for this location.');
				$('.info').css('display','none');
			}
			else
			{
				$('#ans_cont').css('display','');
				$('.info').css('display','');
				if(response["attempts_left"]==-1)
				{
					$('#attempt_left').html('Solved');
					$('#ans_cont').css('display','none');
				}
				else
					$('#attempt_left').html(response["attempts_left"]);
				if(response["attempts_left"]==0)
				{
					$('#ans_cont').css('display','none');
				}
				$('#ques_cont .nano-content').html(response["question"]);
			}
			$('#currLoc,#loc_info').html(destination);
	        panTo([parseFloat(locations[destination]['latitude']),parseFloat(locations[destination]['longitude'])]);
	        setTimeout(function() {
	            open_lb();
	            start_stopwatch(0,0);
	        }, 1500);
		}
		else
		{
			my_alert("This location does not Exist");
		}
	}
	});
}
function ans_submit(answer,currLoc){
	$.ajax({
	type: 'POST',
	data: answer,
	url: server_ip+'api/submit/',
	headers: {'Authorization': "Basic " + user64},
	success: function(response){
		set_score(response["score"]);
		if(response["attempt_status"]==true)
		{
			solved(currLoc);
			$('#ans_cont').css('display','none');
			$('#attempt_left').html('Solved');
			my_alert("Your answer was correct");
		}
		else if(response["attempts_left"]==0)
		{
			blocked(currLoc);
			$('#ans_cont').css('display','none');
			$('#attempt_left').html(response["attempts_left"]);
			my_alert("Your answer was worng and your attempts are over");
		}
		else if(response["attempts_left"]>0){
			wrong(currLoc);
			$('#attempt_left').html(response["attempts_left"]);
			my_alert("Your answer was wrong and you have "+response["attempts_left"]+" attempts left");
		}
	}
	});
}
function loc_distr(){
	$.ajax({
	type: 'GET',
	url: server_ip+'api/loc_distr/',
	headers: {'Authorization': "Basic " + user64},
	success: function(response){
		for(i in response["correct"])
		{
			solved(response["correct"][i]);
		}
		for(i in response["blocked"])
		{
			blocked(response["blocked"][i]);
		}
		for(i in response["wrong"])
		{
			wrong(response["wrong"][i]);
		}
	}
	});
}