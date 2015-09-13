var earth, user, user64="", server_ip,confirm_type=0,place="";
$(function() {
	// server_ip = "http://172.17.1.186:15130/";
	server_ip = "http://192.168.231.108:15130/";

	// form input label animation
	$('.form input').blur(function() {
	    // check if the input has any value (if we've typed into it)
	    if ($(this).val())
	      $(this).addClass('used');
	    else
	      $(this).removeClass('used');
	});
	$('.form input').focus(function(){
		$(this).siblings('.bar').html('');
	})
	$('.form .required').blur(function(){
		if($(this).val()=="")
		{
			$(this).siblings('.bar').html("*Please fill out this field");
		}
	})
	$('.tab a').on('click', function (e) {
		e.preventDefault();
		$(this).parent().addClass('active');
		$(this).parent().siblings().removeClass('active');
		target = $(this).attr('href');
		$('.tab-content > div').not(target).hide();
		$(target).fadeIn(600);
	});
	// form end**************
	$('#ans_cont form').submit(function(e){
		e.preventDefault();
		ans_submit($('#ans_cont input[name="g_answer"]').val(),$('#currLoc').text());
	})
	// Registration/Login form
	$('#reg_form').submit(function(e){
		e.preventDefault();
		var valid = validateReg();
		$('#reg_form input').blur();
		if(valid)
			register($(this));
		return false;
	});
	function validateReg(){
	    var valid = true;
	    var nameReg = /^[A-Za-z\s]+$/;
	    var teamReg = /^[A-Za-z0-9\s]+$/;
	    var numberReg =  /^(\+91|0){0,1}[0-9]{10}$/;
	    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
	    var bitsId = /^20[01]\d(A(\d|B)|B\d){1,2}[PT]S\d\d\d[PHGD]$/;

	    var inputMsg = new Array("*Please fill out this field", "Please use only alphabets ", "Enter a valid ", "ID", "Email","Phone number","or numbers");

	    var check = [
	    	$('.form input[name="name1"]'),
	    	$('.form input[name="bitsid1"]'),
	    	$('.form input[name="email1"]'),
	    	$('.form input[name="phone1"]'),
	    	$('.form input[name="name2"]'),
	    	$('.form input[name="bitsid2"]'),
	    	$('.form input[name="email2"]'),
	    	$('.form input[name="phone2"]'),
	    	$('.form input[name="username"]'),
	    	$('.form input[name="password"]'),
	    ]
	    $('.bar').text('');
	    for(var i=0;i<10;i++)
	    {
	    	switch(i)
	    	{
	    		case 0:
	    		case 4:
	    			if(check[i].val()=="")
	    			{
	    				valid=false;
	    				check[i].siblings('.bar').text(inputMsg[0]);
	    			}
	    			else if(!nameReg.test(check[i].val()))
	    			{
	    				valid=false;
	    				check[i].siblings('.bar').text(inputMsg[1]);
	    			}
	    			break;
	    		case 1:
	    		case 5:
	    			if(check[i].val()!="")
	    			{
	    				if(!bitsId.test(check[i].val().toUpperCase()))
			    			{
			    				valid=false;
			    				check[i].siblings('.bar').text(inputMsg[2] + inputMsg[3]);
			    			}
	    			}
	    			break;
	    		case 2:
	    			if(check[i].val()=="")
	    			{
	    				valid=false;
	    				check[i].siblings('.bar').text(inputMsg[0]);
	    			}
	    			else if(!emailReg.test(check[i].val()))
	    			{
	    				valid=false;
	    				check[i].siblings('.bar').text(inputMsg[2] + inputMsg[4]);
	    			}
	    			break;
	    		case 6:
	    			if(check[i].val()!="")
	    			{
	    				if(!emailReg.test(check[i].val()))
			    			{
			    				valid=false;
			    				check[i].siblings('.bar').text(inputMsg[2] + inputMsg[4]);
			    			}
	    			}
	    			break;
	    		case 3:
	    			if(check[i].val()=="")
	    			{
	    				valid=false;
	    				check[i].siblings('.bar').text(inputMsg[0]);
	    			}
	    			else if(!numberReg.test(check[i].val()))
	    			{
	    				valid=false;
	    				check[i].siblings('.bar').text(inputMsg[2] + inputMsg[5]);
	    			}
	    			break;
	    		case 7:
	    			if(check[i].val()!="")
	    			{
	    				if(!numberReg.test(check[i].val()))
			    			{
			    				valid=false;
			    				check[i].siblings('.bar').text(inputMsg[2] + inputMsg[5]);
			    			}
	    			}
	    			break;
	    		case 8:
	    			if(check[i].val()=="")
	    			{
	    				valid=false;
	    				check[i].siblings('.bar').text(inputMsg[0]);
	    			}
	    			else if(!nameReg.test(check[i].val()))
	    			{
	    				valid=false;
	    				check[i].siblings('.bar').text(inputMsg[1] + inputMsg[6]);
	    			}
	    			break
	    		case 9:
	    			if(check[i].val()=="")
	    			{
	    				valid=false;
	    				check[i].siblings('.bar').text(inputMsg[0]);
	    			}
	    			break;
	    	}
	    }
        return valid;     
	}   
	$('#login_form').submit(function(e){
		e.preventDefault();
		$('#login_form input').blur();
		user = $('#login_form input[name="team_name"]').val();
		if(user==""||$('#login_form input[name="team_password"]').val()=="")
			return;
		user64=window.btoa($('#login_form input[name="team_name"]').val()+':'+$('#login_form input[name="team_password"]').val());
		check_user();
	});
	// form END********************

	$('#sidebar').on('click','.menuitem',function(){
        place = $(this).html();
		my_alert("Are you sure you want to go to "+place,true,1);
    });

});
// Set score
function set_score(x){
	var step_change=0.0;
	var obj =$('#top_team_score');
	var score= parseInt(obj.html());
	if(x>score)
	{
		step_change = parseFloat(x-score)/10;
		for(i=0;i<10;i++){
			setTimeout(function() {
				score = step_change + score;
				obj.text(parseInt(score));
			}, 100*i);
		}
	}
	else if(x<score)
	{
		step_change = parseFloat(score-x)/10;
		for(i=0;i<10;i++){
			setTimeout(function() {
				score = score - step_change;
				obj.text(parseInt(score));
			}, 100*i);
		}
	}
	obj.text(parseInt(x));
}
// setscore END**********
// My alert
function my_alert(message,cancel_disp=true,c_type=0){
	console.log("Alert message: "+message)
	if(cancel_disp)
		$('#alert_cancel').css('display','inline-block');
	else
		$('#alert_cancel').css('display','none');
	confirm_type = c_type;
	$('#alert_message').html(""+message);
	$('#myalert').fadeIn();
	$('#overlay').fadeIn();
}
function confirm_alert(){
	switch(confirm_type){
		case 1:
			if($('#currLoc').text() == place)
				open_lb();
			else
				fly_to(place);
		default:
			close_alert();
	}
}
function close_alert(){
	$('#myalert').fadeOut();
	$('#overlay').fadeOut();
}
// My alert END************
// login
function login_start(){
	console.log('Login started');
	$('#registration_login').fadeOut();
	initialize();
}
// login END******
//Lightbox
function open_lb(){
	$('#overlay').fadeIn();
    $('#ques_lb').fadeIn();
}
function close_lb(){
	$('#ans_cont input').val('');
	$('#overlay').fadeOut();
    $('#ques_lb').fadeOut();
}

//sidebar
var on_sidebar=true;
function sidebar(){
	if(on_sidebar==true)
	{
		$('#sidebar').animate({left:'-210px'},200);
		on_sidebar=false;
	}
	else{
		$('#sidebar').animate({left:'5px'},200);
		on_sidebar=true;
	}
}


// retard############################
// Stopwatch
var sec=0,min=0,time="",s_watch,start=false;
function reset_stopwatch(){
    sec=0;
    min=0;
    time = ((min<10)? "0"+min:min) + ":" + ((sec<10)? "0"+sec:sec);
    $('#stopwatch').html(time);
    $('#timer').html(time);
}
function stop_stopwatch(){
    if(start==true)
    {
        clearInterval(s_watch);
        start=false;
    }
}
function start_stopwatch(tmin,tsec){
	min=tmin;
	sec=tsec;
    if(start==true)
    {
        return false;
    }
    else{
        start=true;
        stopwatch();
    }
}
function stopwatch(){
    sec++;
    if(sec==60)
    {
        sec=0;
        min++;
        if(min==60)
        {
            min=0;
        }
    }
    time = ((min<10)? "0"+min:min) + ":" + ((sec<10)? "0"+sec:sec);
    $('#stopwatch').html(time);
    $('#timer').html(time);
    s_watch = setTimeout(function(){stopwatch();},1000);
}
// stopwatch END******************

//function to Fly to a place
function panTo(coords) {
	earth.panTo(coords,1000);
}

//Intialise the webGl Earth
function initialize() {
	var options = {
		minZoom: 0,
		maxZoom: 5,
		minAltitude:500000,
		maxAltitude: 20000000,
		tileSize: 256,
		bounds: [[-85, -180], [85, 180]],
		tms: true,
	}
	earth = new WE.map('earth_div', options);
	earth.setView([46.8011, 8.2266], 2);
	WE.tileLayer('{z}/{x}/{y}.jpg',options).addTo(earth);
	
	//Displaying Marker
	var marker;
	for (var i in locations) {
		marker = WE.marker([locations[i]['latitude'],locations[i]['longitude']]).addTo(earth);
		marker.bindPopup(
			"<a href = '#' onclick = 'showLightBox()'><div>"+i+"<br><span style='font-size:10px;color:#999'>'Cost of Accomodation: $40/min'</span></div></a>", {maxWidth: 150, closeButton: true});
        $("#sidebar>.nano-content").append('<div class="menuitem" data-place="'+i+'">'+i+'</div>');
        locations[i]["solved"]=0;//0-->not visited,1-->wrong attempt,2-->blocked attempt after many wrong,3-->solved
	};
	$('.nano').nanoScroller();
	$('#top_team_name').text(user);
	user_status();
}