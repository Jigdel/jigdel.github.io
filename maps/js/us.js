
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
		newstate = '<div class="col-md-4 col-xs-4 text-center" id="state-'+i+'"><a href="#" class="map-ques" id="'+allstates[i][2]+'" tabindex="'+(i+1)+'"> <i class="mg map-us-'+allstates[i][1]+' map-detail mg-6x"></i> </a></div>';
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
		scoredescr = "You got every map correct. You know your states from Alabama to Wyoming! Time to tell your friends you know your maps.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/11.png" height="150px" width="260px"></h2>');
	}else if (correctanswers >= 13 && correctanswers <= 15){
		scoretitle = "Such a map nerd, Tamdin! Go ahead jump now :)";
		scoredescr = "Not surprised you know the maps of US states fairly well.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/2.png" height="150px" width="135px"></h2>');
	}else if (correctanswers >= 9 && correctanswers <= 12){
		scoretitle = "Ke garne Tamdin";
		scoredescr = "You did OK, still room for improvement in US states maps marey.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/7.jpg" height="150px" width="260px"></h2>');
	}else if (correctanswers >= 4 && correctanswers <= 8){
		scoretitle = "Ke garne Tamdin but I still love you :)";
		scoredescr = "You did Ok but it looks like you need to study your map of the USA some more marey.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/4.png" height="150px" width="250px"></h2>');
	}else{
		scoretitle = "What happened :( but I still love you more ";
		scoredescr = "Was I distracting you during this quiz haha?";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/6.jpg" height="150px" width="250px"></h2>');
	}
	
	$("#quiz-area").append('<h2 class="text-center score-title">'+scoretitle+'</h2>');
	$("#quiz-area").append('<h4 class="text-center">'+scoredescr+'</4>');
	$("#quiz-area").append('<h3 class="text-center">'+correctanswers+' of 16 Correct</h3>');
	$("#quiz-area").append('<h4 class="text-center score-links"><a href="index.html">Now see how you do with World Maps!</a></h4>');
	$("#quiz-area").append('<p class="text-center score-links"><a href="us.html">Retake the Quiz</a> | <a href="us.html">US State Maps</a></p>');
}

$(document).ready(
	function()
	{
		//available states
		allstates = [ [' Alaska','ak',255],['Alabama','al',254],['Arizona','az',256],['Arkansas','ar',257],['California','ca',258],['Colorado','co',259],['Connecticut','ct',260],['Delaware','de',261],['Florida','fl',262],['Georgia','ga',263],['Hawaii','hi',264],['Idaho','id',265],['Illinois','il',266],['Indiana','in',267],['Iowa','ia',268],['Kansas','ks',269],['Kentucky','ky',270],['Louisiana','la',271],['Maine','me',272],['Maryland','md',273],['Massachusetts','ma',274],['Michigan','mi',275],['Minnesota','mn',276],['Mississippi','ms',277],['Missouri','mo',278],['Montana','mt',279],['Nebraska','ne',280],['Nevada','nv',281],['New Hampshire','nh',282],['New Jersey','nj',283],['New Mexico','nm',284],['New York','ny',285],['North Carolina','nc',286],['North Dakota','nd',287],['Ohio','oh',288],['Oklahoma','ok',289],['Oregon','or',290],['Pennsylvania','pa',291],['Rhode Island','ri',292],['South Carolina','sc',293],['South Dakota','sd',294],['Tennessee','tn',295],['Texas','tx',296],['Utah','ut',297],['Vermont','vt',298],['Virginia','va',299],['Washington','wa',300],['West Virginia','wv',301],['Wisconsin','wi',302],['Wyoming','wy',303] ];
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
					ga('send', 'event', 'USA Quiz Completed', 'click', correctanswers);
				}
				
				return false;
		});
		
		$("body").on("click", "#show-score", function(){
				showscore();
				return false;
		});
		
		$("body").on("click", ".share-fb", function(){
				window.open('https://www.facebook.com/sharer/sharer.php?sdk=joey&u=http%3A%2F%2Fmapglyphs.com%2Fus-map-quiz&display=popup&ref=plugin&src=share_button','sharer','toolbar=0,status=0,width=560,height=455');
				return false;
		});
	
	}
);