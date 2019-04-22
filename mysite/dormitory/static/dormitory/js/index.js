$(function(){
	$("#show").click(function(){
		
		$(".info").css("visibility","visible").toggle()

		
	})
	
	$("#skin").click(function(){
		$(".skin").css("visibility","visible").toggle()
	})
	
	//皮肤

	$("#skin_red").click(function(){
		$(".nav").css("background-color","red")
		$(".info").css("background-color","red")
	})
	$("#skin_plant").click(function(){
		
		$(".nav").css("background-color","#3992d0")
		$(".info").css("background-color","#3992d0")
	})
	$("#skin_black").click(function(){

		$(".nav").css("background-color","black")
		$(".info").css("background-color","black")
	})
})

$(function() {
	$("#menus_area").find("dt").click(function() { //一级菜单点击
		if (!$(this).hasClass("on")) { //当前一级菜单不选中状态才切换
			$("#menus_area").find("dt").removeClass("on");//所有的一级菜单去除选中样式
			$(this).addClass("on");//当前一级菜单去除选中样式
			$('dd').slideUp();//所有二级菜单隐藏
			$(this).nextAll('dd').slideToggle();//当前所有二级菜单切换
		}
	});
})

