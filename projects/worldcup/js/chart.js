function draw(data) {
      /*
        D3.js setup code
      */

          "use strict"; /* Throw out an error - all or nothing */
          
          /* These two variables define position of our chart */
          
          var margin = 35,
              width = 1200 - margin,
              height = 680 - margin;
          
          /*
          var margin = 100, width = 1000 - margin, height = 400 - margin;
          */
          
    	/*debugger; */

          var svg = d3.select("#about")
            .append("svg")
              .attr("width", width + margin)
              .attr("height", height + margin)
              .append('g')
              .attr('class','chart');

      /*
        Dimple.js Chart construction code
      */
          
          /* 'svg' defined above, 'data' passed as argument */
          var myChart = new dimple.chart(svg, data);
          /* Axes */
          var x = myChart.addTimeAxis("x", "year");
          /* Formatting x-axis */
          x.dateParseFormat = "%Y";
          x.tickFormat = "%Y";
          x.timeInterval = 4;
          myChart.addMeasureAxis("y", "attendance");
          
          /* Series */
          /* dimple.plot.bar/scatter/line */
          /* "null" tells Dimple not to facet or group the bars in any way*/
          myChart.addSeries(null, dimple.plot.bar);
          myChart.addSeries("stage", dimple.plot.scatter);
          /* myChart.addSeries("stage", dimple.plot.line); */
          var myLegend = myChart.addLegend(50, 50, 60, 300, "Right");
          myChart.draw();
          
          svg.selectAll("title_text")
          .data(["Legend"])
          .enter()
          .append("text")
            .attr("x", 1310)
            .attr("y", function (d, i) { return 90 + i * 14; })
            .style("font-family", "sans-serif")
            .style("font-size", "10px")
            .style("color", "Black")
            .text(function (d) { return d; });
        	
        };

