function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex ;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}

correctanswers = 0;

currentques = 0;

selectedstate = "";

quizcontinent = "Asia &amp; Oceania";

function placestates(){
	//$(".state-array").html(allstates.toString());
	$(".game-maps").html("");
	selectedstate = "";
	randomstate  = 0;
	randomstate = Math.floor((Math.random() * 3) + 0);
	
	if (randomstate > 3){
		randomstate = 2;	
	}
	//place each state
	for (i = 0; i < 3 ; i++) {
		if (i == randomstate){
			selectedstate = [ allstates[i][0],allstates[i][1],allstates[i][2] ];
			$(".ques-name").html(allstates[i][0]);
			
		}
		newstate = '<div class="col-md-4 col-xs-4 text-center" id="state-'+i+'"><a href="#" class="map-ques" id="'+allstates[i][2]+'" tabindex="'+(i+1)+'"> <i class="mg map-'+allstates[i][1]+' map-detail mg-6x"></i> </a></div>';
    	$(".game-maps").append(newstate);
		allstates.splice(i, 1);
	}
	//alert(allstates.length);
	
}

function updatequesnum(){
	currentques = currentques + 1;
	$(".current-pos").html(currentques);
}

function updatecorrect(){
	correctanswers = correctanswers + 1;
	//$(".num-correct").html(correctanswers);
}

function clearstates(){
	$("#state-0").remove();
	$("#state-1").remove();
	$("#state-2").remove();
}

function showteaser(){
	$("#quiz-area").html("");
	$("#quiz-area").html('<div id="tease-slide"><h3 class="text-center score-title">Your score has been calculated.</h3><p class="text-center">Click the button below to see how you did.</p><p class="text-center"><a class="btn btn-default quiz-btn" href="#" id="show-score">Show me my score</a></p></div>');
}

function showscore(){
	$("#quiz-area").html("");
	
	scoretitle = "";
	scoredescr = "";
	
	
	if (correctanswers == 16){
		scoretitle = "Tamdin you're map genius! Your pala would have been proud of you :)";
		scoredescr = "You answered every question correct. You know "+quizcontinent+" inside and out!";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/11.png" height="170px" width="254px"></h2>');
	}else if (correctanswers >= 13 && correctanswers <= 15){
		scoretitle = "Such a map nerd, Tamdin! Go ahead jump now :)";
		scoredescr = "Not surprised you know the maps of "+quizcontinent+" fairly well.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/2.png" height="160px" width="171px"></h2>');
	}else if (correctanswers >= 9 && correctanswers <= 12){
		scoretitle = "Ke garne Tamdin";
		scoredescr = "You did OK, still room for improvement in "+quizcontinent+" maps marey.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/7.jpg" height="160px" width="284px"></h2>');
	}else if (correctanswers >= 4 && correctanswers <= 8){
		scoretitle = "Ke bhayo Tamdin but I still love you :)";
		scoredescr = "You did OK, still room for improvement in "+quizcontinent+" maps marey.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/4.png" height="160px" width="259px"></h2>');
	}else{
		scoretitle = "What happened :( but I still love you more ";
		scoredescr = "Was I distracting you during this map of "+quizcontinent+"? ;)";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/6.jpg" height="160px" width="284"></h2>');
	}
	
	$("#quiz-area").append('<h2 class="text-center score-title">'+scoretitle+'</h2>');
	$("#quiz-area").append('<h4 class="text-center">'+scoredescr+'</4>');
	$("#quiz-area").append('<h3 class="text-center">'+correctanswers+' of 16 Correct</h3>');
	$("#quiz-area").append('<h4 class="text-center score-links"><a href="africa.html">Now see how you do with maps of Africa!</a></h4>');
	$("#quiz-area").append('<p class="text-center score-links"><a href="asia.html">Retake the Quiz</a> | <a href="asia.html">Maps of Asia</a> </p>');
}

$(document).ready(
	function()
	{
		
		

		//available states
		allstates = [ ['Afghanistan','af',1],['Bangladesh','bd',19],['Bhutan','bt',26],['British Indian Ocean Territory','io',33],['Brunei Darussalam','bn',34],['Cambodia','kh',38],['China','cn',46],['East Timor','tl',221],['Hong Kong','hk',99],['India','in',102],['Indonesia','id',103],['Japan','jp',111],['Kazakhstan','kz',114],['Kyrgyzstan','kg',120],['Laos','la',121],['Macau','mo',130],['Malaysia','my',134],['Mongolia','mn',147],['Myanmar','mm',152],['Nepal','np',155],['North Korea','kp',117],['Pakistan','pk',167],['Philippines','ph',174],['Singapore','sg',199],['South Korea','kr',118],['Sri Lanka','lk',209],['Taiwan','tw',217],['Tajikistan','tj',218],['Thailand','th',220],['Turkmenistan','tm',228],['Uzbekistan','uz',238],['Vietnam','vn',242],['Australia','au',14],['Christmas Island','cx',47],['Guam','gu',90],['New Caledonia','nc',157],['New Zealand','nz',158],['Papua New Guinea','pg',171],['Vanuatu','vu',239],['Antarctica','aq',9],['Bouvet Island','bv',31],['Falkland Islands','fk',72],['Australian Capital Territory','au-ac',327],['New South Wales','au-nw',321],['Northern Territory','au-nt',328],['Queensland','au-ql',322],['South Australia','au-sa',323],['Tasmania','au-ts',324],['Victoria','au-vc',325],['Western Australia','au-wa',326],['Fiji','fj',74] ];
		shuffle(allstates);
		updatequesnum();
		placestates();
		
		$("body").on("click", "a.map-ques", function(){
				thisstateid = $(this).attr("id");
				if (thisstateid == selectedstate[2]){
					updatecorrect();
				}
				clearstates();
				if (currentques <= 15){
					updatequesnum();
					placestates();
				}else{
					showteaser();
					ga('send', 'event', 'Asia Quiz Completed', 'click', correctanswers);
				}
				
				return false;
		});
		
		$("body").on("click", "#show-score", function(){
				showscore();
				return false;
		});
		
		$("body").on("click", ".share-fb", function(){
				window.open('https://www.facebook.com/sharer/sharer.php?sdk=joey&u=http%3A%2F%2Fmapglyphs.com%2Fasia-map-quiz&display=popup&ref=plugin&src=share_button','sharer','toolbar=0,status=0,width=560,height=455');
				return false;
		});
	
	}
);