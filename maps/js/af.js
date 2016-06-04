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

quizcontinent = "Africa &amp the Middle East";

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
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/11.png" height="170" width="260"></h2>');
	}else if (correctanswers == 15){
		scoretitle = "So close but you expected that marah.";
		scoredescr = "Maybe you'll get the full score on "+quizcontinent+" maps in the next try!";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/noworries.jpg" height="150px" width="205"></h2>');
	}else if (correctanswers == 14){
		scoretitle = "Such a map nerd, Tamdin! Go ahead jump now :)";
		scoredescr = "Not surprised you know the maps of "+quizcontinent+" fairly well.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/2.png" height="150px" width="185"></h2>');
	}else if (correctanswers == 13){
		scoretitle = "Am I thaaat distracting?";
		scoredescr = "Was I distracting you during this map of "+quizcontinent+" quiz? ;)";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/smile.jpg" height="150px" width="205"></h2>');
	}else if (correctanswers == 12){
		scoretitle = "I blame it on the chipmunks!";
		scoredescr = "Sure you'll do well in this "+quizcontinent+" maps next round.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/chipmunks.jpg" height="150px" width="205"></h2>');
	}else if (correctanswers == 11){
		scoretitle = "Not a bad score, you don't need to run.";
		scoredescr = "Sure you'll do well in this "+quizcontinent+" maps next round.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/run.jpg" height="150px" width="205"></h2>');
	}else if (correctanswers == 10){
		scoretitle = "Not a bad score, why so serious?";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/serious.jpg" height="150px" width="205"></h2>');
	}else if (correctanswers == 9){
		scoretitle = "Here's a kiss for your favorite number.";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/4.png" height="150px" width="135"></h2>');
	}else if (correctanswers == 8){
		scoretitle = "Just a random laugh picture, why not marah?";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/1.png" height="200px" width="155"></h2>');
	}else if (correctanswers == 7){
		scoretitle = "Someone needs to try harder ..";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/tryharder.jpg" height="150px" width="265"></h2>');
	}else if (correctanswers == 6){
		scoretitle = "6 is bollywood breeze time!";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/breeze.jpg" height="150px" width="215"></h2>');
	}else if (correctanswers == 5){
		scoretitle = "Five is red jacket on fire..";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/uhuh.jpg" height="200px" width="155"></h2>');
	}else if (correctanswers == 4){
		scoretitle = "4 is 4 freezing on Liberty!";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/liberty.jpg" height="150px" width="205"></h2>');
	}else if (correctanswers == 3){
		scoretitle = "Three times in the rain! ";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/rain.jpg" height="150px" width="205"></h2>');
	}else if (correctanswers == 2){
		scoretitle = "2 of us on train!";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/train.jpg" height="150px" width="205"></h2>');
	}else if (correctanswers == 1){
		scoretitle = "Maybe we need to study world map again.";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/world.jpg" height="200px" width="155"></h2>');
	}else{
		scoretitle = "What happened :( but I still love you more ";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/6.jpg" height="160px" width="284"></h2>');
	}
	
	$("#quiz-area").append('<h2 class="text-center score-title">'+scoretitle+'</h2>');
	$("#quiz-area").append('<h4 class="text-center">'+scoredescr+'</4>');
	$("#quiz-area").append('<h3 class="text-center">'+correctanswers+' of 16 Correct</h3>');
	$("#quiz-area").append('<h4 class="text-center score-links"><a href="americas.html">Now see how you do with maps of the Americas!</a></h4>');
	$("#quiz-area").append('<p class="text-center score-links"><a href="/africa.html">Retake the Quiz</a> | <a href="africa.html">Maps of Africa</a> | <a href="/middle-east">Maps of the Middle East</a></p>');
}

$(document).ready(
	function()
	{
		
		

		//available states
		allstates = [ ['Algeria','dz',4],['Angola','ao',7],['Benin','bj',24],['Botswana','bw',30],['Burkina Faso','bf',36],['Burundi','bi',37],['Cameroon','cm',39],['Cape Verde','cv',41],['Central African Republic','cf',43],['Chad','td',44],['Comoros','km',50],['Congo','cg',51],['Democratic Republic of the Congo','cd',52],['Djibouti','dj',62],['Egypt','eg',66],['Equatorial Guinea','gq',68],['Eritrea','er',69],['Ethiopia','et',71],['Gabon','ga',80],['Gambia','gm',81],['Ghana','gh',84],['Guinea','gn',93],['Guinea-Bissau','gw',94],['Ivory Coast','ci',55],['Kenya','ke',115],['Lesotho','ls',124],['Liberia','lr',125],['Libya','ly',126],['Madagascar','mg',132],['Malawi','mw',133],['Mali','ml',136],['Mauritania','mr',140],['Mauritius','mu',141],['Morocco','ma',150],['Mozambique','mz',151],['Namibia','na',153],['Niger','ne',160],['Nigeria','ng',161],['Rwanda','rw',183],['Senegal','sn',195],['Sierra Leone','sl',198],['Somalia','so',204],['South Africa','za',205],['South Sudan','ss',207],['Sudan','sd',210],['Swaziland','sz',213],['Tanzania','tz',219],['Togo','tg',222],['Tunisia','tn',226],['Uganda','ug',231],['Western Sahara','eh',246],['Bahrain','bh',18],['Iran','ir',104],['Iraq','iq',105],['Israel','il',108],['Jordan','jo',113],['Kuwait','kw',119],['Lebanon','lb',123],['Oman','om',166],['Qatar','qa',179],['Saudi Arabia','sa',194],['State of Palestine','ps',169],['Syria','sy',216],['United Arab Emirates','ae',233],['Yemen','ye',247] ];
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
					ga('send', 'event', 'Africa Quiz Completed', 'click', correctanswers);
				}
				
				return false;
		});
		
		$("body").on("click", "#show-score", function(){
				showscore();
				return false;
		});
		
		$("body").on("click", ".share-fb", function(){
				window.open('https://www.facebook.com/sharer/sharer.php?sdk=joey&u=http%3A%2F%2Fmapglyphs.com%2Fafrica-map-quiz&display=popup&ref=plugin&src=share_button','sharer','toolbar=0,status=0,width=560,height=455');
				return false;
		});
	
	}
);