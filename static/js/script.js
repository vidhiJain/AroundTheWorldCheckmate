var earth, user, user64="", server_ip,confirm_type=0,place="";
$(function() {
	server_ip = "http://172.17.1.186:15130/";
	// server_ip = "http://192.168.231.108:15130/";

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
		my_alert("Are you sure you want to go to "+place+" ?<br>"+get_loc_detail(place),1,true);
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
				if(obj.css('background-color')=="rgb(42, 179, 42)")
				{
					obj.css('background-color','');
				}
				else
				{
					obj.css('background-color','rgb(42, 179, 42)');
				}
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
				if(obj.css('background-color')=="rgb(179, 42, 42)")
				{
					obj.css('background-color','');
				}
				else
				{
					obj.css('background-color','rgb(179, 42, 42)');
				}
			}, 100*i);
		}
	}
}
// setscore END**********
function solved(loc){
	locations[loc]["solved"]=3;//solved
	var sidebarloc = $('#sidebar>.nano-content>div[data-place="'+loc+'"');
	sidebarloc.removeClass('wrong');
	sidebarloc.addClass('solved');
	$('div[data-placem="'+loc+'"] .we-pm-icon').css('background-image','url("./img/markerG.png")');
}
function blocked(loc){
	locations[loc]["solved"]=2;//blocked
	var sidebarloc = $('#sidebar>.nano-content>div[data-place="'+loc+'"');
	sidebarloc.removeClass('wrong');
	sidebarloc.addClass('blocked');
	$('div[data-placem="'+loc+'"] .we-pm-icon').css('background-image','url("./img/markerR.png")');
}
function wrong(loc){
	locations[loc]["solved"]=1;//wrong
	var sidebarloc = $('#sidebar>.nano-content>div[data-place="'+loc+'"');
	sidebarloc.addClass('wrong');
	$('div[data-placem="'+loc+'"] .we-pm-icon').css('background-image','url("./img/markerY.png")');
}
// My alert
function my_alert(message,c_type=0,cancel_disp=false){
	console.log("Alert message: "+message)
	if(cancel_disp){
		$('#alert_cancel').css('display','inline-block');
		$('#alert_ok').text('Confirm');
	}
	else
	{
		$('#alert_cancel').css('display','none');
		$('#alert_ok').text('OK');
	}
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
    $('#ques_cont').nanoScroller();
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
		minAltitude:2000000,
		maxAltitude: 20000000,
		tileSize: 256,
		bounds: [[-85, -180], [85, 180]],
		tms: true,
		sky: true,
	}
	earth = new WE.map('earth_div', options);
	earth.setView([46.8011, 8.2266], 2);
	WE.tileLayer('{z}/{x}/{y}.jpg',options).addTo(earth);
	
	//Displaying Marker
	var marker;
	for (var i in locations) {
		marker = WE.marker([locations[i]['latitude'],locations[i]['longitude']]).addTo(earth);
		myAddPopup(marker["element"],i);
		$(marker["element"]).attr('data-placem', i);
        $("#sidebar>.nano-content").append('<div class="menuitem" data-place="'+i+'">'+i+'</div>');
        locations[i]["solved"]=0;//0-->not visited,1-->wrong attempt,2-->blocked attempt after many wrong,3-->solved
	};
	
	$('#earth_div>div').click(function(){
		if($(this).find('.e_popup').css('visibility')=="visible")
		{
			$(this).find('.e_popup').css({'visibility':'hidden','opacity':'0'});
		}
		else
		{
			$(this).find('.e_popup').css({'visibility':'visible','opacity':'1'});
			$(this).siblings().find('.e_popup').css({'visibility':'hidden','opacity':'0'});
		}
	});
	$('.e_pu_wc_go').click(function(){
		place = $(this).siblings('.e_pu_wc_top-bar').html();
		my_alert("Are you sure you want to go to "+place+" ?<br>"+get_loc_detail(place),1,true);
	});
	$('.e_popup_close').click(function(){
		$('.e_popup').css('opacity','0');
	});

	$('#sidebar').nanoScroller();
	$('#top_team_name').text(user);
	user_status();
	loc_distr();
}
function myAddPopup(elem,i){
	var popup='<div class="e_popup"> <div class="e_popup_close" >&times;</div><div class="e_pu_wrapper"> <div class="e_pu_w_content"><div class="e_pu_wc_top-bar">'+i+'</div><div class="e_pu_wc_disp">'+get_loc_detail(i)+'</div><div class="e_pu_wc_go">GO</div></div> </div> <div class="e_pu_tip_cont"> <div class="tip"></div> </div> </div>'
	$(elem).append(popup);
	return;
}
function get_loc_detail(i){
	return 'Country: '+locations[i]["country"]+'<br>Travel Cost: '+(2*3)+'<br>Rent: '+locations[i]["rent"]+'<br>Stipend: '+locations[i]["stipend"];
}