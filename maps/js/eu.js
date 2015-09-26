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

quizcontinent = "Europe";

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
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/11.png" height="150px" width="260"></h2>');
	}else if (correctanswers >= 13 && correctanswers <= 15){
		scoretitle = "Such a map nerd, Tamdin! Go ahead jump now :)";
		scoredescr = "Not surprised you know the maps of "+quizcontinent+" fairly well.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/2.png" height="150px" width="260"></h2>');
	}else if (correctanswers >= 9 && correctanswers <= 12){
		scoretitle = "Ke garne Tamdin";
		scoredescr = "You did OK, still room for improvement in "+quizcontinent+" maps marey.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/7.jpg" height="150px" width="260"></h2>');
	}else if (correctanswers >= 4 && correctanswers <= 8){
		scoretitle = "Ke garne Tamdin but I still love you :)";
		scoredescr = "You did OK, still room for improvement in "+quizcontinent+" maps marey.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/4.png" height="150px" width="250"></h2>');
	}else{
		scoretitle = "What happened :( but I still love you more ";
		scoredescr = "Was I distracting you during this map of "+quizcontinent+"? ;)";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/6.jpg" height="150px" width="250"></h2>');
	}
	
	$("#quiz-area").append('<h2 class="text-center score-title">'+scoretitle+'</h2>');
	$("#quiz-area").append('<h4 class="text-center">'+scoredescr+'</4>');
	$("#quiz-area").append('<h3 class="text-center">'+correctanswers+' of 16 Correct</h3>');
	$("#quiz-area").append('<h4 class="text-center score-links"><a href="asia.html">Now see how you do with Asia and Pacific maps!</a></h4>');
	$("#quiz-area").append('<p class="text-center score-links"><a href="eu.html">Retake the Quiz</a> | <a href="eu.html">Maps of '+quizcontinent+'</a></p>');
}

$(document).ready(
	function()
	{
		
		

		//available states
		allstates = [ ['Albania','al',3],['Armenia','am',12],['Austria','at',15],['Azerbaijan','az',16],['Belarus','by',21],['Belgium','be',22],['Bosnia and Herzegovina','ba',29],['Bulgaria','bg',35],['Croatia','hr',56],['Cyprus','cy',59],['Czech Republic','cz',60],['Denmark','dk',61],['Estonia','ee',70],['Finland','fi',75],['France','fr',76],['Georgia','ge',82],['Germany','de',83],['Gibraltar','gi',85],['Greece','gr',86],['Greenland','gl',87],['Guernsey','gg',92],['Hungary','hu',100],['Iceland','is',101],['Republic of Ireland','ie',106],['Italy','it',109],['Jersey','je',112],['Kosovo','xk',355],['Latvia','lv',122],['Liechtenstein','li',127],['Lithuania','lt',128],['Luxembourg','lu',129],['Macedonia','mk',131],['Malta','mt',137],['Moldova','md',145],['Monaco','mc',146],['Montenegro','me',148],['Netherlands','nl',156],['Norway','no',165],['Poland','pl',176],['Portugal','pt',177],['Romania','ro',181],['Russia','ru',182],['San Marino','sm',192],['Serbia','rs',196],['Slovakia','sk',201],['Slovenia','si',202],['Spain','es',208],['Sweden','se',214],['Switzerland','ch',215],['Turkey','tr',227],['Ukraine','ua',232],['United Kingdom','uk',234],['England','uk-en',305],['Northern Ireland','uk-ni',306],['Scotland','uk-sc',307],['Wales','uk-wa',308] ];
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
					ga('send', 'event', 'Europe Quiz Completed', 'click', correctanswers);
				}
				
				return false;
		});
		
		$("body").on("click", "#show-score", function(){
				showscore();
				return false;
		});
		
		$("body").on("click", ".share-fb", function(){
				window.open('https://www.facebook.com/sharer/sharer.php?sdk=joey&u=http%3A%2F%2Fmapglyphs.com%2Feurope-map-quiz&display=popup&ref=plugin&src=share_button','sharer','toolbar=0,status=0,width=560,height=455');
				return false;
		});
	
	}
);