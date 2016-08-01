{% load i18n %}

function format_users(users, num_anonymous) {
	var content = '<ul class="list-group">';
	content = content+'<li class="list-group-item active">{% trans "Actually online" %}</li>';
	content = content+'<li class="list-group-item">';
	//console.log("USERS: "+users);
	for (var i = 0; i < users.length; i++) {
		user = users[i];
	    //console.log("USER: "+user);
	    content = content+'<div><i class="fa fa-user" style="color:lightgrey"></i> '+user+'<div>';
	};
	content = content+'</li>';
	var num_anonymous = parseFloat(num_anonymous);
	if ( num_anonymous > 0) {
		if ( num_anonymous == 1) {
			content = content+'<li class="list-group-item">+ '+num_anonymous+" {% trans 'anonymous user' %}"+'</li>';
		}
		else {
			content = content+'<li class="list-group-item">+ '+num_anonymous+" {% trans 'anonymous users' %}"+'</li>';
		}
	}
	content = content+'</ul>';
	return content
}