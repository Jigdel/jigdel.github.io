function draw(data) {
      
      /*
        D3.js setup code
      */

          "use strict"; /* Throw out an error - all or nothing */
          var margin = 75,
              width = 1400 - margin,
              height = 600 - margin;
		
		  var radius = 3;
		  var color = 'blue';
		  var multiplier = 1.3;
		  
          // d3.select("body")
          //   .append("h2")
          //   .text("World Cup Attendance")

          var svg = d3.select("body")
            .append("svg")
              .attr("width", width + margin)
              .attr("height", height + margin)
            .append('g')
                .attr('class','chart');

      /*
        Dimple.js Chart construction code
      */

          d3.select("svg")
            .selectAll("circle")
            .data(data)
            .enter()
            .append("circle");

          // Find range of date column
          var time_extent = d3.extent(data, function(d) {
              return d['date'];
          });

          // Find range of attendance column
          var count_extent = d3.extent(data, function(d) {
              return d['attendance'];
          })

		  //Using d3.extent to return max, min values for scales
          // Create x-axis scale mapping dates -> pixels
          var time_scale = d3.time.scale()
            .range([margin, width]) //left & right most part of chart
            .domain(time_extent);

          // Create y-axis scale mapping attendance -> pixels
          var count_scale = d3.scale.linear()
            .range([height, margin]) //inverted coordinated plane of SVG
            .domain(count_extent);

          // Creating x-axis using .axis() function
          var time_axis = d3.svg.axis()
            .scale(time_scale)
            .ticks(d3.time.years, 2);
            //ticks every two yrs
          	//ticks every day .tick(d3.time.days

          var count_axis = d3.svg.axis()
            .scale(count_scale)
            .orient("left");

          d3.select("svg")
            .append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(time_axis);

          d3.select("svg")
            .append("g")
            .attr("class", "y axis")
            .attr("transform", "translate(" + margin + ",0)")
            .call(count_axis);
            //notice inverted coordinates again

          //debugger;

            d3.selectAll("circle")
            .attr("cx", function(d) {
                return time_scale(d["date"]);
            })
            .attr("cy", function(d) {
                return count_scale(d["attendance"]);
            })
            .attr("r", function(d) {
            		if (d['home'] == d['team1'] ||  d['home'] == d['team2']) {
            		return radius * multiplier;
            		}
            		else {
            			return radius; 
            			}
            		})
            .attr("fill", function(d) {
            		if (d['home'] == d['team1'] ||  d['home'] == d['team2']) {
            			return 'red';
            		}
            		else {
            			return 'blue';
            			}
            		})
            
            // set the stage for the legend with the SVG elements
            var legend = svg.append("g")
            				.attr("class", "legend")
            				.attr("transform", "translate(" + (width - 100) + "," + 20 + ")") //20px down from top - remember inverted coordinates
            				.selectAll("g")
            				.data(["Home Team", "Others"])
            				.enter().append("g");
            
            var legend = svg.append("g")
              .attr("class", "legend")
              .attr("transform", "translate(" + (width - 100) + "," + 20 + ")")
              .selectAll("g")
              .data(["Home Team", "Others"])
              .enter().append("g");

          legend.append("circle")
          // d-> datum, i-> index so [0]-> "Home Team"
              .attr("cy", function(d, i) {
                  return i * 30;
              })
              .attr("r", function(d) {
            			if (d == "Home Team") {
            				return radius * multiplier;
            			} else {
            				return radius;
            			}
            		})
            	.attr("fill", function(d) {
            			if (d == "Home Team") {
            				return 'red';
            			} else {
            				return 'blue';
            			}
            		});

          legend.append("text")
              .attr("y", function(d, i) {
                  return i * 30 + 5;
              })
              .attr("x", radius * 5)
              .text(function(d) {
                  return d;
              });			
    };