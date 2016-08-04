{% load i18n %}

function format_users(users, num_anonymous) {
	var content = '<ul style="list-style:none">';
	content = content+'<li style="display:inline-block;color:grey">Online:</li>';
	content = content+'<li style="display:inline-block;padding:0 0.5em 0 0.5em">';
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
			content = content+'<li style="display:inline-block;padding:0 0.5em 0 0.5em">+ '+num_anonymous+" anonyme"+'</li>';
		}
		else {
			content = content+'<li style="display:inline-block;padding:0 0.5em 0 0.5em">+ '+num_anonymous+" {% trans 'anonymous users' %}"+'</li>';
		}
	}
	content = content+'</ul>';
	return content
}