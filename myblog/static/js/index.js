//画布大小
	var width = 800;
	var height = 600;
	var heights=500;

	//在 body 里添加一个 SVG 画布
	var svg = d3.select("#svgdiv")
		.append("svg")
		.attr("width", width)
		.attr("height", height);

    // var title=svg.append("g")
    // .append("text")
    // .attr("class","title")
    // .text("设备主人管辖设备统计")
    // .attr({
    //     "x":200,
    //     "y":530
    // });

	//画布周边的空白
	var padding = {left:30, right:30, top:30, bottom:30};

	//定义一个数组
	var dataset = data1;

	//x轴的比例尺
	var xScale = d3.scale.ordinal()
		.domain(d3.range(dataset.length))
		.rangeRoundBands([0, width - padding.left - padding.right]);

	//y轴的比例尺
	var yScale = d3.scale.linear()
		.domain([0,d3.max(dataset)+5])
		.range([heights - padding.top - padding.bottom, 0]);

	//定义x轴
	var xAxis = d3.svg.axis()
		.scale(xScale)
		.orient("bottom");

	//定义y轴
	var yAxis = d3.svg.axis()
		.scale(yScale)
		.orient("left");

	//矩形之间的空白
	var rectPadding = 4;


	//添加x轴
	svg.append("g")
		.attr("class","axisx")
		.attr("transform","translate(" + padding.left + "," + (heights - padding.bottom) + ")")
		.call(xAxis);

	//添加y轴
	svg.append("g")
		.attr("class","axisy")
		.attr("transform","translate(" + padding.left + "," + padding.top + ")")
		.call(yAxis);
	//添加矩形元素


//x轴
    var textx = svg.selectAll(".MyX")
		.data(xd)
		.enter()
		.append("text")
		.attr("class","MyX")
		// .attr("transform","translate(" + padding.left + "," + padding.top + ")")
		.attr("x", function(d,i){
			return xScale(i);
		} )
		.attr("y",heights - padding.top - padding.bottom-3)
		.attr("dx",40)
		.attr("dy",53)
		.text(function(d){
			return d;
		});

    var rects = svg.selectAll(".MyRect")
		.data(dataset)
		.enter()
		.append("rect")
		.attr("class","MyRect")
		.attr("transform","translate(" + padding.left + "," + padding.top + ")")
		.attr("x", function(d,i){
			return xScale(i) + rectPadding/2;
		} )
		.attr("width", xScale.rangeBand() - rectPadding )
        .attr("y",function(d){
			var min = yScale.domain()[0];
			return yScale(min);
		})
		.attr("height", function(d){
			return 0;
		})
        .attr("fill","steelblue")		//填充颜色不要写在CSS里
		.on("mouseover",function(d,i){
			d3.select(this)
				.attr("fill","green");
		})
		.on("mouseout",function(d,i){
			d3.select(this)
				.transition()
		        .duration(500)
				.attr("fill","steelblue");
		})
        .transition()
		.delay(function(d,i){
			return i * 200;
		})
		.duration(2000)
		.ease("bounce")
		.attr("y",function(d){
			return yScale(d);
		})
		.attr("height", function(d){
			return heights - padding.top - padding.bottom - yScale(d);
		});


	//添加文字元素
	var texts = svg.selectAll(".MyText")
		.data(dataset)
		.enter()
		.append("text")
		.attr("class","MyText")
		.attr("transform","translate(" + padding.left + "," + padding.top + ")")
		.attr("x", function(d,i){
			return xScale(i) + rectPadding/2;
		} )
		.attr("y",function(d){
			return yScale(d);
		})
		.attr("dx",function(){
			return (xScale.rangeBand() - rectPadding)/2;
		})
		.attr("dy",function(d){
			return 20;
		})
		.text(function(d){
			return d;
		});