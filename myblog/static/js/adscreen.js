	function adjustToFreezeWidth(rootSvg) {  
    var windowWidth = $(window).width();  
	var viewBoxVal = rootSvg.getAttribute("viewBox");  
    rootSvg.removeAttribute("width");  
    rootSvg.removeAttribute("height");  
    var setWidth = windowWidth;  
    var setHeight = (setWidth * 9) / 16;  
    rootSvg.setAttribute("width", setWidth);  
    rootSvg.setAttribute("height", setHeight);  
	}  
	
    $(function () {
	    var svgRootDom = $("#jlcsvg")[0];  
		var svgRootDom0 = $("#jllbcsvg")[0];
		var svgRootDom1 = $("#hlbzlcsvg")[0];  
		var svgRootDom2 = $("#zydsvg")[0]; 		
		var svgRootDom3= $("#ecsbsvg")[0]; 	
		adjustToFreezeWidth(svgRootDom);  
        adjustToFreezeWidth(svgRootDom0);  
		adjustToFreezeWidth(svgRootDom1); 
		adjustToFreezeWidth(svgRootDom2); 
		adjustToFreezeWidth(svgRootDom3); 
    });    //调整屏幕尺寸