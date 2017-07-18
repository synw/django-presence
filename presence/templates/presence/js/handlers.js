{% load i18n %}

if (event_class == '__presence__') {
	var users = data["users"];
	var anonymous = data["anonymous"];
	{% include "presence/js/utils.js" %}
	var content=format_users(users, anonymous);
	document.getElementById("presencebox").innerHTML = content;
	return false
}