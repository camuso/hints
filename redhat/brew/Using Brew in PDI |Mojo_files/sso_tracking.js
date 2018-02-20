$j(document).ready(function() {
	$j("img[data-src*='solution-tracker']").each(function(i)
	{
		try
		{
			var tmp_username = window._jive_current_user.username || document.getElementsByClassName('jive-avatar')[0].dataset.username;
			$j(this).attr("src", $j(this).attr("data-src")+"?user="+tmp_username);
		}catch(e)
		{}
	});
});
