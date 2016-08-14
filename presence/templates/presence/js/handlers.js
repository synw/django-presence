if (event_class == '__presence__') {
	console.log('Presence event');
	var s = message.split('/');
	var users = s[0].split(',');
	var anonymous = s[1];
	var content=format_users(users, anonymous);
	$('#presencebox').html(content);
	return false
}