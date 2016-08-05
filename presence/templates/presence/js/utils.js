{% load i18n %}

var debug = true;

function format_users(users, num_anonymous) {
	var content = '<ul style="list-style:none">';
	content = content+'<li style="display:inline;color:grey">Online:</li>';
	if (debug === true) {console.log("USERS: "+users)};
	if (users.length > 0) {
		for (var i = 0; i < users.length; i++) {
			user = users[i];
			if (debug === true) {console.log("USER: "+user)};
		    content = content+'<li style="display:inline;padding:0 0.5em 0 0.5em"><i class="fa fa-user" style="color:lightgrey"></i> '+user+'</li>';
		};
	}
	var num_anonymous_ = parseFloat(num_anonymous);
	if ( num_anonymous > 0) {
		if (debug === true) {console.log(num_anonymous_)};
		if ( num_anonymous_ == 1) {
			content = content+'<li style="display:inline;padding:0 0.5em 0 0.5em"> '+num_anonymous+" {% trans 'anonymous user' %}"+'</li>';
		}
		else {
			content = content+'<li style="display:inline;padding:0 0.5em 0 0.5em"> '+num_anonymous+" {% trans 'anonymous users' %}"+'</li>';
		}
	}
	content = content+'</ul>';
	return content
}