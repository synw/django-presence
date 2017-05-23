{% load i18n %}

if (event_class == '__presence__') {
	var s = message.split('/');
	var users = s[0].split(',');
	var anonymous = s[1];
	{% include "presence/js/utils.js" %}
	var content=format_users(users, anonymous);
	document.getElementById("presencebox").innerHTML = content;
	return false
}