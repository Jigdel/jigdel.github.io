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

quizcontinent = "Americas";

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
	$("#quiz-area").append('<h4 class="text-center score-links"><a href="us.html">Now see how you do with US State maps!</a></h4>');
	$("#quiz-area").append('<p class="text-center score-links"><a href="americas.html">Retake the Quiz</a> | <a href="americas.html">Maps of the '+quizcontinent+'</a></p>');
}

$(document).ready(
	function()
	{
		
		

		//available states
		allstates = [ ['Canada','ca',40],['Mexico','mx',143],['United States','us-alt',354],['Cuba','cu',57],['Trinidad and Tobago','tt',225],['Haiti','ht',96] ,['Argentina','ar-alt',361],['Bolivia','bo',27],['Brazil','br',32],['Chile','cl',45],['Colombia','co',49],['Ecuador','ec',65],['French Guiana','gf',77],['Guyana','gy',95],['Paraguay','py',172],['Peru','pe',173],['Suriname','sr',211],['Uruguay','uy',237],['Venezuela','ve',241],['Belize','bz',23],['Costa Rica','cr',54],['El Salvador','sv',67],['Guatemala','gt',91],['Honduras','hn',98],['Nicaragua','ni',159],['Panama','pa',170],['Alberta','ca-ab',309],['British Columbia','ca-bc',310],['Manitoba','ca-mb',311],['New Brunswick','ca-nb',312],['Newfoundland and Labrador','ca-nl',356],['Northwest Territories','ca-nt',318],['Nova Scotia','ca-ns',313],['Nunavut','ca-nu',319],['Ontario','ca-on',314],['Prince Edward Island','ca-pe',315],['Quebec','ca-qc',316],['Saskatchewan','ca-sk',317],['Yukon','ca-yt',320],['Dominican Republic','do',64],['Aruba','aw',13],['Curacao','cw',58],['Saint Kitts and Nevis','kn',186],['Puerto Rico','pr',178],['Bermuda','bm',25],['Guadeloupe','gp',89],['US Virgin Islands','vi',244],['British Virgin Islands','vg',243],['Jamaica','jm',110],['Sint Maarten','sx',200],['Saint Martin','mf',188],['Bahamas','bs',17],['Barbados','bb',20] ];
		
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
					ga('send', 'event', 'Americas Quiz Completed', 'click', correctanswers);
				}
				
				return false;
		});
		
		$("body").on("click", "#show-score", function(){
				showscore();
				return false;
		});
		
		$("body").on("click", ".share-fb", function(){
				window.open('https://www.facebook.com/sharer/sharer.php?sdk=joey&u=http%3A%2F%2Fmapglyphs.com%2Famericas-map-quiz&display=popup&ref=plugin&src=share_button','sharer','toolbar=0,status=0,width=560,height=455');
				return false;
		});
	
	}
);