    var width  = 800;	//SVG绘制区域的宽度
	var height = 600;	//SVG绘制区域的高度
    var heights =500;

	var svg = d3.select("#svgdiv3")			//选择<body>
				.append("svg")			//在<body>中添加<svg>
				.attr("width", width)	//设定<svg>的宽度属性
				.attr("height", height);//设定<svg>的高度属性

	//1. 确定初始数据
	var datasetstack = data3;


	//2. 转换数据
	var stack = d3.layout.stack()
					.values(function(d){ return d.importance; })
					.x(function(d){ return d.name; })
					.y(function(d){ return d.profit; });

	var datastack= stack(datasetstack);

	console.log(datastack);

	//3. 绘制

	//外边框
	var padding = { left:50, right:100, top:30, bottom:30 };

	//创建x轴比例尺
	var xRangeWidth = width - padding.left - padding.right;

	var xScale = d3.scale.ordinal()
					.domain(datastack[0].importance.map(function(d){ return d.name; }))
					.rangeBands([0, xRangeWidth],0.05);

	//创建y轴比例尺

	//最大利润（定义域的最大值）
	var maxProfit = d3.max(datastack[datastack.length-1].importance, function(d){
							return d.y0 + d.y;
					});

	//最大高度（值域的最大值）
	var yRangeWidth = heights - padding.top - padding.bottom;

	var yScale = d3.scale.linear()
					.domain([0, maxProfit])		//定义域
					.range([0, yRangeWidth]);	//值域


	//颜色比例尺
	// var color = d3.scale.category10();
    var color =["green","steelblue","orange","red"];
	//添加分组元素
	var groups = svg.selectAll("g")
					.data(datastack)
					.enter()
					.append("g")
					.style("fill",function(d,i){ return color[i]; });

	//添加矩形
	var rects = groups.selectAll("rect")
					.data(function(d){ return d.importance; })
					.enter()
					.append("rect")
					.attr("x",function(d){ return xScale(d.name); })
					.attr("y",function(d){ return yRangeWidth - yScale( d.y0 + d.y ); })
					.attr("width",function(d){ return xScale.rangeBand(); })
					.attr("height",function(d){ return yScale(d.y); })
					.attr("transform","translate(" + padding.left + "," + padding.top + ")");

	rects.append("title").text(function(d){return d.profit;});

	//添加坐标轴
	var xAxis = d3.svg.axis()
				.scale(xScale)
				.orient("bottom");

	yScale.range([yRangeWidth, 0]);

	var yAxis = d3.svg.axis()
					.scale(yScale)
					.orient("left");

	svg.append("g")
			.attr("class","stackaxisx")
			.attr("transform","translate(" + padding.left + "," + (heights - padding.bottom) +  ")")
			.call(xAxis);

	svg.append("g")
			.attr("class","stackaxisy")
			.attr("transform","translate(" + padding.left + "," + (heights - padding.bottom - yRangeWidth) +  ")")
			.call(yAxis);

	svg.append("g")
    .append("text")
    .attr("class","title")
    .text("按设备管控级别统计")
    .attr({
        "x":200,
        "y":530
    });

	//添加分组标签
	var labHeight = 50;
	var labRadius = 10;

	var labelCircle = groups.append("circle")
						.attr("cx",function(d){ return width - padding.right*0.98; })
						.attr("cy",function(d,i){ return padding.top * 2 + labHeight * (3-i); })
						.attr("r",labRadius);

	var labelText = groups.append("text")
						.attr("x",function(d){ return width - padding.right*0.8; })
						.attr("y",function(d,i){ return padding.top * 2 + labHeight * (3-i); })
						.attr("dy",labRadius/2)
						.text(function(d){ return d.name; });