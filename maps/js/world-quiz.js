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

quizcontinent = "World";

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
	}else if (correctanswers == 15){
		scoretitle = "So close but you expected that marah.";
		scoredescr = "Maybe you'll get the full score on "+quizcontinent+" maps in the next try!";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/noworries.jpg" height="150px" width="135"></h2>');
	}else if (correctanswers == 14){
		scoretitle = "Such a map nerd, Tamdin! Go ahead jump now :)";
		scoredescr = "Not surprised you know the maps of "+quizcontinent+" fairly well.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/2.png" height="150px" width="135"></h2>');
	}else if (correctanswers == 13){
		scoretitle = "Am I thaaat distracting?";
		scoredescr = "Was I distracting you during this map of "+quizcontinent+"? ;)";scoredescr = " "+quizcontinent+" f";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/smile.jpg" height="150px" width="135"></h2>');
	}else if (correctanswers == 12){
		scoretitle = "I blame it on the chipmunks!";
		scoredescr = "Sure you'll do well in this "+quizcontinent+" maps next round.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/chipmunks.jpg" height="150px" width="135"></h2>');
	}else if (correctanswers == 11){
		scoretitle = "Not a bad score, you don't need to run.";
		scoredescr = "Sure you'll do well in this "+quizcontinent+" maps next round.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/run.jpg" height="150px" width="135"></h2>');
	}else if (correctanswers == 10){
		scoretitle = "Not a bad score, why so serious?";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/serious.jpg" height="150px" width="135"></h2>');
	}else if (correctanswers == 9){
		scoretitle = "Here's a kiss for your favorite number.";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/4.jpg" height="150px" width="135"></h2>');
	}else if (correctanswers == 8){
		scoretitle = "Just a random laugh picture, why not marah?";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/1.png" height="150px" width="135"></h2>');
	}else if (correctanswers == 7){
		scoretitle = "Someone needs to try harder ..";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/harder.jpg" height="150px" width="135"></h2>');
	}else if (correctanswers == 6){
		scoretitle = "6 is bollywood breeze time!";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/breeze.jpg" height="150px" width="135"></h2>');
	}else if (correctanswers == 5){
		scoretitle = "Five is red jacket on fire..";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/uhuh.jpg" height="150px" width="135"></h2>');
	}else if (correctanswers == 4){
		scoretitle = "4 is 4 freezing on Liberty!";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/liberty.jpg" height="150px" width="135"></h2>');
	}else if (correctanswers == 3){
		scoretitle = "Threellled shot! ";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/1.png" height="150px" width="135"></h2>');
	}else if (correctanswers == 2){
		scoretitle = "2 of us on train!";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/train.jpg" height="150px" width="135"></h2>');
	}else if (correctanswers == 1){
		scoretitle = "Maybe we need to study world map again.";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/world.jpg" height="150px" width="135"></h2>');
	}else{
		scoretitle = "What happened :( but I still love you more ";
		scoredescr = "I'm sure you just did this on "+quizcontinent+" quiz to see the picture.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/6.jpg" height="150px" width="250"></h2>');
	}

/*	if (correctanswers == 16){
		scoretitle = "Tamdin you're map genius! Your pala would have been proud of you :)";
		scoredescr = "You answered every question correct. You know "+quizcontinent+" inside and out!";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/11.png" height="150px" width="260"></h2>');
	}else if (correctanswers >= 13 && correctanswers <= 15){
		scoretitle = "Such a map nerd, Tamdin! Go ahead jump now :)";
		scoredescr = "Not surprised you know the maps of "+quizcontinent+" fairly well.";
		$("#quiz-area").append('<h2 class="text-center score-title"><img src="img/2.png" height="150px" width="135"></h2>');
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
	}*/
	
	$("#quiz-area").append('<h2 class="text-center score-title">'+scoretitle+'</h2>');
	$("#quiz-area").append('<h4 class="text-center">'+scoredescr+'</4>');
	$("#quiz-area").append('<h3 class="text-center">'+correctanswers+' of 16 Correct</h3>');
	$("#quiz-area").append('<h4 class="text-center score-links"><a href="eu.html">Now see how you do with maps of Europe!</a></h4>');
	$("#quiz-area").append('<p class="text-center score-links"><a href="index.html">Retake the Quiz</a> | <a href="index.html">Maps of the '+quizcontinent+'</a></p>');
}

$(document).ready(
	function()
	{
		
		

		//available states
		allstates = [ ['Afghanistan','af',1],['Bangladesh','bd',19],['Bhutan','bt',26],['Brunei Darussalam','bn',34],['Cambodia','kh',38],['China','cn',46],['East Timor','tl',221],['Hong Kong','hk',99],['India','in',102],['Indonesia','id',103],['Japan','jp',111],['Kazakhstan','kz',114],['Kyrgyzstan','kg',120],['Laos','la',121],['Macau','mo',130],['Malaysia','my',134],['Mongolia','mn',147],['Myanmar','mm',152],['Nepal','np',155],['North Korea','kp',117],['Pakistan','pk',167],['Philippines','ph',174],['Singapore','sg',199],['South Korea','kr',118],['Sri Lanka','lk',209],['Taiwan','tw',217],['Tajikistan','tj',218],['Thailand','th',220],['Turkmenistan','tm',228],['Uzbekistan','uz',238],['Vietnam','vn',242],['Albania','al',3],['Armenia','am',12],['Austria','at',15],['Azerbaijan','az',16],['Belarus','by',21],['Belgium','be',22],['Bosnia and Herzegovina','ba',29],['Bulgaria','bg',35],['Croatia','hr',56],['Cyprus','cy',59],['Czech Republic','cz',60],['Denmark','dk',61],['Estonia','ee',70],['Finland','fi',75],['France','fr',76],['Georgia','ge',82],['Germany','de',83],['Gibraltar','gi',85],['Greece','gr',86],['Greenland','gl',87],['Guernsey','gg',92],['Hungary','hu',100],['Iceland','is',101],['Republic of Ireland','ie',106],['Italy','it',109],['Jersey','je',112],['Kosovo','xk',355],['Latvia','lv',122],['Liechtenstein','li',127],['Lithuania','lt',128],['Luxembourg','lu',129],['Macedonia','mk',131],['Malta','mt',137],['Moldova','md',145],['Monaco','mc',146],['Montenegro','me',148],['Netherlands','nl',156],['Norway','no',165],['Poland','pl',176],['Portugal','pt',177],['Romania','ro',181],['Russia','ru',182],['San Marino','sm',192],['Serbia','rs',196],['Slovakia','sk',201],['Slovenia','si',202],['Spain','es',208],['Sweden','se',214],['Switzerland','ch',215],['Turkey','tr',227],['Ukraine','ua',232],['United Kingdom','uk',234],['England','uk-en',305],['Northern Ireland','uk-ni',306],['Scotland','uk-sc',307],['Wales','uk-wa',308],['Argentina','ar-alt',361],['Bolivia','bo',27],['Brazil','br',32],['Chile','cl',45],['Colombia','co',49],['Ecuador','ec',65],['French Guiana','gf',77],['Guyana','gy',95],['Paraguay','py',172],['Peru','pe',173],['Suriname','sr',211],['Uruguay','uy',237],['Venezuela','ve',241],['Australia','au',14],['Christmas Island','cx',47],['Guam','gu',90],['New Caledonia','nc',157],['New Zealand','nz',158],['Papua New Guinea','pg',171],['Vanuatu','vu',239],['Algeria','dz',4],['Angola','ao',7],['Benin','bj',24],['Botswana','bw',30],['Burkina Faso','bf',36],['Burundi','bi',37],['Cameroon','cm',39],['Cape Verde','cv',41],['Central African Republic','cf',43],['Chad','td',44],['Comoros','km',50],['Congo','cg',51],['Democratic Republic of the Congo','cd',52],['Djibouti','dj',62],['Egypt','eg',66],['Equatorial Guinea','gq',68],['Eritrea','er',69],['Ethiopia','et',71],['Gabon','ga',80],['Gambia','gm',81],['Ghana','gh',84],['Guinea','gn',93],['Guinea-Bissau','gw',94],['Ivory Coast','ci',55],['Kenya','ke',115],['Lesotho','ls',124],['Liberia','lr',125],['Libya','ly',126],['Madagascar','mg',132],['Malawi','mw',133],['Mali','ml',136],['Mauritania','mr',140],['Mauritius','mu',141],['Morocco','ma',150],['Mozambique','mz',151],['Namibia','na',153],['Niger','ne',160],['Nigeria','ng',161],['Rwanda','rw',183],['Senegal','sn',195],['Sierra Leone','sl',198],['Somalia','so',204],['South Africa','za',205],['South Sudan','ss',207],['Sudan','sd',210],['Swaziland','sz',213],['Tanzania','tz',219],['Togo','tg',222],['Tunisia','tn',226],['Uganda','ug',231],['Western Sahara','eh',246],['Zambia','zm',248],['Zimbabwe','zw',249],['Antarctica','aq',9],['Bouvet Island','bv',31],['Falkland Islands','fk',72],['Belize','bz',23],['Costa Rica','cr',54],['El Salvador','sv',67],['Guatemala','gt',91],['Honduras','hn',98],['Nicaragua','ni',159],['Panama','pa',170],['Bahrain','bh',18],['Iran','ir',104],['Iraq','iq',105],['Israel','il',108],['Jordan','jo',113],['Kuwait','kw',119],['Lebanon','lb',123],['Oman','om',166],['Qatar','qa',179],['Saudi Arabia','sa',194],['State of Palestine','ps',169],['Syria','sy',216],['United Arab Emirates','ae',233],['Yemen','ye',247],['Canada','ca',40],['Mexico','mx',143],['United States','us-alt',354],['Cuba','cu',57],['Trinidad and Tobago','tt',225],['Haiti','ht',96],['Aruba','aw',13],['Dominican Republic','do',64],['Curacao','cw',58],['Bermuda','bm',25],['Guadeloupe','gp',89],['Saint Kitts and Nevis','kn',186],['Puerto Rico','pr',178],['US Virgin Islands','vi',244],['British Virgin Islands','vg',243] ];
		
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
					ga('send', 'event', 'World Quiz Completed', 'click', correctanswers);
				}
				
				return false;
		});
		
		$("body").on("click", "#show-score", function(){
				showscore();
				return false;
		});
		
		$("body").on("click", ".share-fb", function(){
				window.open('https://www.facebook.com/sharer/sharer.php?sdk=joey&u=http%3A%2F%2Fmapglyphs.com%2Fworld-map-quiz&display=popup&ref=plugin&src=share_button','sharer','toolbar=0,status=0,width=560,height=455');
				return false;
		});
	
	}
);