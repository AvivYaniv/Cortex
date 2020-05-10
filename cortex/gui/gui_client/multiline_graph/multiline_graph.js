
var multiline_graph = function (graph_raw_data, dictConfiguration) {
  // ********************* Sizes Section ***********************
  var dictGraphSize = {
    width: 800,
    height: 600,
  };

  var dictGraphMargin = {
      top: 20,
      right: 80,
      bottom: 150,
      left: 50,
    },
    nRectWidth =
      dictGraphSize.width - dictGraphMargin.left - dictGraphMargin.right,
    nRectHeight =
      dictGraphSize.height - dictGraphMargin.top - dictGraphMargin.bottom;

  // ********************* Dates Section ***********************
  var parseDate = function (d) { return new Date(d) };
  var dpDateParserForMovingMouse = d3.time.format(dictConfiguration.mouse_legend_date_format);

  // ********************* Scales Section ***********************
  var xScale = d3.time.scale().range([0, nRectWidth]).nice();
  var yScale = d3.scale.linear().range([nRectHeight, 0]).nice();

  var color = d3.scale.category10();

  var x_axis_date_format = dictConfiguration.hasOwnProperty('x_axis_date_format') ? dictConfiguration.x_axis_date_format : "%d %b";

  var xAxis = d3.svg.axis().scale(xScale).orient("bottom").tickFormat(d3.time.format(x_axis_date_format));
  var yAxis = d3.svg.axis().scale(yScale).orient("left");

  // ********************* Data Section ***********************
  function rename_json_field(json_object, old_name, new_name)
  {
    String.prototype.replaceAll = function(f,r){return this.split(f).join(r);}
    return JSON.parse(JSON.stringify(json_object).replaceAll(old_name, new_name));
  }

  var graph_parsed_data = graph_raw_data;

  // In order to enable user to have any name for date colum, where d3 demands predefined name, we change it based on configuration to the predefined name
  if (!dictConfiguration.hasOwnProperty("date_colum_name")) 
  {
    dictConfiguration.push({
        key:   "date_colum_name",
        value: "_datetime"
    });
  }
  else{
    graph_parsed_data = rename_json_field(graph_raw_data, dictConfiguration.date_colum_name, "_datetime");
  }

  var lGraphLine = d3.svg
    .line()
    .interpolate("cardinal")
    .x(function (d) {      
      return xScale(d._datetime);
    })
    .y(function (d) {      
      return yScale(d.category_value);
    });

  // ********************* X-Axis Data Section *****************
  var tDateTicks = graph_parsed_data.map(function (d) {
    return parseDate(d._datetime);
  });

  var tDateOriginalTicks = graph_parsed_data.map(function (d) {
    return d._datetime;
  });

  var tIDTicks = graph_parsed_data.map(function (d) {
    return d[dictConfiguration.id_column_name];
  });

  var g = d3
    .select('#' + dictConfiguration.element_id)
    .append("svg")
    .attr("width", nRectWidth + dictGraphMargin.left + dictGraphMargin.right)
    .attr("height", nRectHeight + dictGraphMargin.top + dictGraphMargin.bottom)
    .append("g");

  var svg = g.attr(
    "transform",
    "translate(" + dictGraphMargin.left + "," + dictGraphMargin.top + ")"
  );

  color.domain(
    d3.keys(graph_parsed_data[0]).filter(function (key) {
      return (key !== "_datetime") && (key != dictConfiguration.id_column_name);
    })
  );

  graph_parsed_data.forEach(function (d) {
    d._datetime = parseDate(d._datetime);
  });

  var categories = color.domain().map(function (name) {    
    return {
      name: name,
      predefined_color : dictConfiguration.hasOwnProperty('predefined_colors_dictionary') ? ( dictConfiguration.predefined_colors_dictionary.hasOwnProperty(name) ? dictConfiguration.predefined_colors_dictionary[name] : undefined) : undefined,
      values: graph_parsed_data.map(function (d) {
        return {
          _datetime : d._datetime,
          _name : name,
          predefined_color : dictConfiguration.hasOwnProperty('predefined_colors_dictionary') ? ( dictConfiguration.predefined_colors_dictionary.hasOwnProperty(name) ? dictConfiguration.predefined_colors_dictionary[name] : undefined) : undefined,
          uuid: d[dictConfiguration.id_column_name],
          category_value: +d[name],
        };
      }),
    };
  });

  xScale.domain(
    d3.extent(graph_parsed_data, function (d) {
      return d._datetime;
    })
  );
 
  if (dictConfiguration.hasOwnProperty('y_axis_extent'))
  {
    var y_axis_extent = dictConfiguration.y_axis_extent;
    yScale.domain(dictConfiguration.y_axis_extent);
  }
  else
  {
    yScale.domain([
      d3.min(categories, function (c) {
        return d3.min(c.values, function (v) {
          return v.category_value;
        });
      }),
      d3.max(categories, function (c) {
        return d3.max(c.values, function (v) {
          return v.category_value;
        });
      }),
    ]);
  }

  if (dictConfiguration.show_lines_rect_legend)
  {
    var legend = svg
    .selectAll("g")
    .data(categories)
    .enter()
    .append("g")
    .attr("class", "legend");

  legend
    .append("rect")
    .attr("x", nRectWidth - 20)
    .attr("y", function (d, i) {
      return i * 20;
    })
    .attr("width", 10)
    .attr("height", 10)
    .style("fill", function (d) {
      return d.predefined_color ? d.predefined_color : color(d.name);
    });

  legend
    .append("text")
    .attr("x", nRectWidth - 8)
    .attr("y", function (d, i) {
      return i * 20 + 9;
    })
    .text(function (d) {
      return d.name;
    });
  }

  // xAxis Legend
  svg
    .append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + nRectHeight + ")")
    .call(xAxis)
    .selectAll("text")	
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-65)");

  // yAxis Legend
  svg
    .append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text(dictConfiguration.y_axis_legend);

  var category = svg
    .selectAll(".category")
    .data(categories)
    .enter()
    .append("g")
    .attr("class", "category");
  
  category
    .append("path")
    .attr("class", "line")
    .attr("d", function (d) {
      return lGraphLine(d.values);
    })
    .style("stroke", function (d) {
      return d.predefined_color ? d.predefined_color : color(d.name);
    });

  // Adding dots on sampling points
  category
    .selectAll(".dot")
    .data(function(d) {
      return d.values
    })
    .enter()
    .append("circle")
    .attr("r", 3)
    .attr("cx", function(d, i) {
      return xScale(d._datetime);
    })
    .attr("cy", function(d) {
      return yScale(d.category_value);
    })
    .attr("fill", function(d) {
      return d.predefined_color ? d.predefined_color : color(d._name);
    })
    ;

  category
    .append("text")
    .datum(function (d) {
      return {
        name: d.name,
        value: d.values[d.values.length - 1],
      };
    })
    .attr("transform", function (d) {
      return (
        "translate(" +
        xScale(d.value._datetime) +
        "," +
        yScale(d.value.category_value) +
        ")"
      );
    })
    .attr("x", 3)
    .attr("dy", ".35em")
    .text(function (d) {
      return d.name;
    });

  var mouseG = svg.append("g").attr("class", "mouse-over-effects");

  // This is the black vertical line to follow mouse
  mouseG
    .append("path")
    .attr("class", "mouse-line darkable")    
    .style("stroke", "black")
    .style("stroke-width", "1px")
    .style("opacategory", "0");

  var lLinesValues = document.getElementsByClassName("line");

  var mousePerLine = mouseG
    .selectAll(".mouse-per-line")
    .data(categories)
    .enter()
    .append("g")
    .attr("class", "mouse-per-line");

  // Circle over mouse moving vertical line intersection with graph lines
  mousePerLine
    .append("circle")
    .attr("r", 3)
    .style("stroke", function (d) {
      return d.predefined_color ? d.predefined_color : color(d.name);
    })
    .style("fill", "none")
    .style("stroke-width", "1px")
    .style("opacategory", "0");

  mousePerLine.append("text").attr("transform", "translate(10,3)");

  mouseG
    .append("svg:rect") // append a rect to catch mouse movements on canvas
    .attr("width", nRectWidth) // can't catch mouse events on a g element
    .attr("height", nRectHeight)
    .attr("fill", "none")
    .attr("pointer-events", "all")
    .on("mouseout", function () {
      // on mouse out hide line, circles and text
      d3.select(".mouse-line").style("opacategory", "0");
      d3.selectAll(".mouse-per-line circle").style("opacategory", "0");
      d3.selectAll(".mouse-per-line text").style("opacategory", "0");
    })
    .on("mouseover", function () {
      // on mouse in show line, circles and text
      d3.select(".mouse-line").style("opacategory", "1");
      d3.selectAll(".mouse-per-line circle").style("opacategory", "1");
      d3.selectAll(".mouse-per-line text").style("opacategory", "1");
    })
    .on("mousemove", function () {
      // mouse moving over canvas
      var mouse = d3.mouse(this);

      // TODO : callback function to further investigate
      if (dictConfiguration.hasOwnProperty("mouse_moving_callback")) 
      {
            var xPosition = new Date(xScale.invert(mouse[0]));

            var tickPos = tDateTicks;
            function find_mouses_x_axis_value(m) 
            {
                m_orig = m;
                m = m.getTime();
                var lowDiff = 1e99;
                var xI = null;
                for (var i = 0; i < tickPos.length; i++) 
                {
                    var current = new Date(tickPos[i].toString()).getTime();
                    var diff = Math.abs(m - current);
                    if (diff < lowDiff) 
                    {
                        lowDiff = diff;
                        xI = i;                        
                    }
                }                
                return [ tIDTicks[xI] , tDateTicks[xI], lowDiff ];
            };
            
            // Finding closest x axis position and id
            var cpClosestPosition = find_mouses_x_axis_value(xPosition);

            if (null !== cpClosestPosition)
            {
              // Call callback
              dictConfiguration["mouse_moving_callback"](cpClosestPosition);
            }
        }
        
      d3.select(".mouse-line").attr("d", function () {
        var d = "M" + mouse[0] + "," + nRectHeight;
        d += " " + mouse[0] + "," + 0;
        return d;
      });

      d3.selectAll(".mouse-per-line").attr("transform", function (d, i) {
        var xDate = xScale.invert(mouse[0]);
        bisect = d3.bisector(function (d) {
          return d._datetime;
        }).right;
        idx = bisect(d.values, xDate);

        var beginning = 0,
          end = lLinesValues[i].getTotalLength(),
          target = null;

        while (true) {
          target = Math.floor((beginning + end) / 2);
          pos = lLinesValues[i].getPointAtLength(target);
          if ((target === end || target === beginning) && pos.x !== mouse[0]) {
            break;
          }
          if (pos.x > mouse[0]) end = target;
          else if (pos.x < mouse[0]) beginning = target;
          else break; //position found
        }

        d3.select(this)
          .select("text")
          .text(
            yScale.invert(pos.y).toFixed(2) +              
              dpDateParserForMovingMouse(xDate)
          );

        return "translate(" + mouse[0] + "," + pos.y + ")";
      });
    });
};
