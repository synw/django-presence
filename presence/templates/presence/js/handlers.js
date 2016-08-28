{% load i18n %}

if (event_class == '__presence__') {
	var s = message.split('/');
	var users = s[0].split(',');
	var anonymous = s[1];
	var content=format_users(users, anonymous);
	$('#presencebox').html(content);
	return false
}