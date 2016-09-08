subscription.presence().then(function(message) {
	//if ( debug === true ) {console.log('PRESENCE: '+JSON.stringify(message.data))};
	var uinfo = count_users(message.data);
	var users = uinfo[0];
	var anonymous = uinfo[1];
	var content = format_users(users, anonymous);
	$('#presencebox').html(content);
}, function(err) {
	if ( debug === true ) {console.log('PRESENCE ERROR: '+err)};
});