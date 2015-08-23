function draw_bar_graph(json_data) {
    var total_data_points = json_data["data_points"].length;
    var svg_div = "#" + json_data["meta"]["svg_div_id"];
    var svg_div_container = '.' + json_data["meta"]["svg_div_container"];

    if (json_data["meta"]["time_dependent"] == "True")
        var time_dependent = true;
    else
        var time_dependent = false;


    // acquiring svg dimensions from parent div
    var svgWidth = $(svg_div_container).parent().width();
    var svgHeight = $(svg_div_container).parent().height();

    if(time_dependent) {
        var parseDate = d3.time.format(json_data["meta"]["strftime_string"]).parse;
    }

    // assigning svg dimensions if explicitely specified in json_data["meta"]
    if(json_data["meta"]["height"]) {
        var svgHeight = parseInt(json_data["meta"]["height"]);
    }
    if(json_data["meta"]["width"]) {
        var svgWidth = parseInt(json_data["meta"]["width"]);
    }

    var margin = {
        top: 20,
        right: 10,
        bottom: 50,
        left: 60
    };

    // reduce left and bottom margins if x_label and y_label are not provided
    if(!json_data["meta"]["x_label"]) {
        margin.bottom = 25;
    }
    if(!json_data["meta"]["y_label"]) {
        margin.left = 40;
    }


    // plot dimensions
    var plotWidth = svgWidth - margin.left - margin.right;
    var plotHeight = svgHeight - margin.top - margin.bottom;

    //tooltip
    var tip = d3.tip()
            .attr('class', 'd3-tip')
            .offset([-10, 0])
            .html(function(d) {
                if(time_dependent) {
                    var date = parseDate(d.x_value)
                    var date_string = d3.time.format("%e %b, %H:%M")(date);
                    return date_string + ": <span style=\"color:yellow;\">" + d.y_value + "</span>";
                }
                else {
                    return d.x_value + ": <span style=\"color:yellow;\">" + d.y_value + "</span>";
                }
            });


    var svg = d3.select(svg_div)
            .append("svg")
            .attr("width", svgWidth)
            .attr("height", svgHeight)
            .attr('class', 'line-graph-svg')
            .call(tip);

    if(time_dependent) {
        // start and end timestamps for xScale
        var start_timestamp = json_data['meta']['start_timestamp'];
        var end_timestamp = json_data['meta']['end_timestamp'];

        // pick up start and end timestamp from json_data.data_points if not
        // explicitely provided
        if(total_data_points > 0) {
            if(!start_timestamp) {
                start_timestamp = json_data["data_points"][0]["x_value"]
            }
            if(!end_timestamp) {
                end_timestamp = json_data["data_points"][total_data_points-1]["x_value"]
            }
        }

        // dot points on line graph
        // only some of the points need to be selected since json_data.data_point might be huge.
        if(total_data_points > 0) {
            var seperation = 35;
            var no_of_circles = parseInt(plotWidth/seperation);

            var date_diff = (parseDate(end_timestamp) - parseDate(start_timestamp)) / no_of_circles;

            var selected_data_points = [];

            var diff_counter = 0;

            var date_reference = parseDate(start_timestamp);
            for(var i = 0; i < total_data_points; i++) {
                var diff = parseDate(json_data.data_points[i].x_value) - date_reference;
                if(diff >= 0) {
                    selected_data_points.push(json_data.data_points[i]);
                    date_reference = new Date(date_reference.getTime() + date_diff);
                }
            }
            selected_data_points.push(json_data.data_points[total_data_points-1]);
        }
    }
    else {
        var selected_data_points = json_data.data_points;
    }


    if(time_dependent) {
        var xScale = d3.time.scale()
            .domain([
                parseDate(start_timestamp),
                parseDate(end_timestamp)
            ])
            .range([0, plotWidth]);
    }
    else {
       var xticks = []
       for(var i=0; i<total_data_points; i++ ) {
           xticks.push(json_data['data_points'][i]['x_value'])
       }
       var xScale = d3.scale.ordinal()
            .domain(xticks)
            .rangeRoundBands([0, svgWidth-margin.right-margin.left])
    }

    var max_count = d3.max(json_data['data_points'], function(d) { return d.y_value; });

    // increase max_count slightly to keep some space on the top of the plot
    max_count += max_count * 0.15;
    var yScale = d3.scale.linear()
            .domain([0, max_count])
            .range([plotHeight, 0]);

    var xTicks = parseInt(plotWidth/50);

    if(time_dependent) {
        // reduce the no of ticks to show on xAxis to make them readable
        var ticks_to_show = [];
        for(var i = 0; i < selected_data_points.length-1; i+=2) {
            ticks_to_show.push(selected_data_points[i]);
        }

        var xAxis = d3.svg.axis()
            .scale(xScale)
            .tickValues(ticks_to_show.map(function(d) { return parseDate(d.x_value); }))
            .tickFormat(d3.time.format("%e %b"))
            .orient("bottom");
    }
    else {
        var xAxis = d3.svg.axis()
            .scale(xScale)
            .orient("bottom");
    }

    var yAxis = d3.svg.axis()
            .scale(yScale)
            .ticks(plotHeight/30)
            .orient("left");


    // drawing gridlines
    svg.append("g")
            .attr("transform", "translate(" + margin.left  + "," + margin.top + ")")
            .selectAll(".grid")
            .data(new Array(Math.ceil(plotWidth/10)))
            .enter().append("line")
            .attr("class", "grid")
            .attr("x1", function(d, i) { return i*10; })
            .attr("x2", function(d, i) { return i*10; })
            .attr("y1", 0)
            .attr("y2", plotHeight)

    svg.append("g")
            .attr("transform", "translate(" + margin.left  + "," + margin.top + ")")
            .selectAll(".grid")
            .data(new Array(Math.ceil(plotHeight/10)))
            .enter().append("line")
            .attr("class", "grid")
            .attr("x1", 0)
            .attr("x2", plotWidth)
            .attr("y1", function(d, i) { return i*10; })
            .attr("y2", function(d, i) { return i*10; })

    // append x axis to the svg
    svg.append("g")
            .attr("class", "x-axis")
            .attr("transform", "translate(" + margin.left + ", " + (plotHeight+20) + ")")
            .call(xAxis)
          .append("text")
            .attr("class", "axis-label")
            .style("text-anchor", "middle")
            .attr("x", (svgWidth - margin.left - margin.right - 10)/2)
            .attr("y", 40)
            .text(json_data["meta"]["x_label"]);

    // append y axis to the svg
    svg.append("g")
            .attr("class", "y-axis")
            .attr("transform", "translate(" + margin.left + ", " + margin.top + ")")
            .call(yAxis)
          .append("text")
            .attr("class", "axis-label")
            .attr("transform", "rotate(-90)")
            .style("text-anchor", "middle")
            .attr("x", margin.top - svgHeight/2)
            .attr("y", -40)
            .text(json_data["meta"]["y_label"]);

    // right dotted y axis
    var right_yAxis = d3.svg.axis()
            .scale(yScale)
            .tickFormat("")
            .orient("right");

    // append right dotted y axis to the svg
    svg.append("g")
            .attr("class", "y-axis dotted")
            .attr("transform", "translate(" + (svgWidth - margin.right) + ", " + margin.top + ")")
            .style("stroke-dasharray", 6)
            .call(right_yAxis)

    var bar_width = (plotWidth-total_data_points*10)/total_data_points;

    // svg continuous path, primary line graph
    svg.selectAll(".bar")
            .data(json_data["data_points"])
          .enter().append("rect")
            .attr("class", "bar-graph")
            .attr("x", function(d, i, j){  return 5+xScale(d.x_value); })
            .attr("y", function(d) { return yScale(d.y_value); })
            .attr("width", bar_width)
            .attr("height", function(d) { return plotHeight - yScale(d.y_value); })
            .attr("transform", "translate(" + margin.left  + ", " + margin.top + ")")
            .on('mouseover', function(d) {
                d3.select(this).transition()
                    .duration(500)
                    .style('fill', 'rgba(114, 178, 105, 0.9)');

                tip.show(d);
            })
            .on('mouseout', function() {
                d3.select(this).transition()
                    .duration(500)
                    .style('fill', 'rgba(114, 178, 105, 0.6)');

                tip.hide();
            });
}
