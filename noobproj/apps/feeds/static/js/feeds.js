$(document).ready(function() {
	// body...
	/*function hide_stream_update(){
		$(".stream-update").hide();


	};*/

	$(".btn-compose").click(function(){
		if($(".compose").hasClass("composing")){
			$(".compose").removeClass("composing");
			$(".compose").slideUp();
		}
		else{
			$(".compose").addClass("composing");
			$(".compose").slideDown(function(){
				$(".compose textarea").focus();
			});
		}
		$(".compose").show();
	});
	$(".btn-cancel-compose").click(function(){
		if($(".compose").hasClass("composing")){
			$(".compose").removeClass("composing");
			$(".compose").slideUp();
		}
	});

	$(".btn-post").click(function(){
		var last_feed = $(".stream li:first-child").attr("feed-id");
		if(last_feed == undefined){
			last_feed = "0";
		}
		$("#compose-form input[name='last_feed']").val(last_feed);
		$.ajax({
			url: '/feeds/new/',
			data: $("#compose-form").serialize(),
			type: "post",
			cache: false,
			success: function (data){
				$("ul.stream").prepend(data);
        		$(".compose").slideUp();
        		$(".compose").removeClass("composing");
        		//hide_stream_update();
			}
		});
	});

	$("ul.stream").on("click", ".remove-feed", function(){
		var li = $(this).closest("li")
		var feed = $(li).attr("feed-id");
		var csrf = $(li).attr("csrf");
		$.ajax({
			url: '/feeds/delete/',
			data: {
					'feed': feed,
        			'csrfmiddlewaretoken': csrf
				},
			type: 'post',
			cache: false,
			success: function(){
       			$(li).fadeOut(400, function () {
          		$(li).remove();
        		});
			}
		});
	});

	$("ul.stream").on("click", ".comment", function () { 
	    var post = $(this).closest(".post");
	    if ($(".comments", post).hasClass("tracking")) 
	    {
	      $(".comments", post).slideUp();
	      $(".comments", post).removeClass("tracking");
	    }
	    else {
	      $(".comments", post).show();
	      $(".comments", post).addClass("tracking");
	      $(".comments input[name='post']", post).focus();
	      var feed = $(post).closest("li").attr("feed-id");
	      $.ajax({
	        url: '/feeds/comment/',
	        data: { 'feed': feed },
	        cache: false,
	        beforeSend: function () {
	          $("ol", post).html("<li class='loadcomment'>loading....</li>");
	        },
	        success: function (data) {
	          $("ol", post).html(data);
	          $(".comment-count", post).text($("ol li", post).not(".empty").length);
	        }
	      		});
	    	}
	    return false;
		  });

	$("ul.stream").on("keydown", ".comments input[name='post']", function (evt) {
		var keyCode = evt.which?evt.which:evt.keyCode; 
		if (keyCode == 13)
		 {
		 	var form = $(this).closest('form');
		 	var container = $(this).closest(".comments");
		 	var input = $(this);
		 	$.ajax({
		 		url: '/feeds/comment/',
		 		type: 'post',
		 		data: $(form).serialize(),
		 		cache: false,
		 		beforeSend: function(){
		 			$(input).val("");},
		 		success: function (data) {
		 			// body...
		 			$("ol", container).html(data);
			        var post_container = $(container).closest(".post");
			        $(".comment-count", post_container).text($("ol li", container).length);
		 		}

		 	})
		 	
		 }

		});


});
