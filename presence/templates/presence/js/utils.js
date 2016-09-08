{% load i18n %}

var debug = false;

function count_users(presence_info) {
	var users = [];
	var anonymous = 0;
	for (var key in presence_info) {
		  if (presence_info.hasOwnProperty(key)) {
			var user = presence_info[key].user;
			if (user == "") {
				anonymous++;
			}
			else {
				users.push(user);
			}
		  }
		}
	if ( debug === true ) {console.log("Users: "+users+' + '+anonymous+' anonymous')};
	return [users, anonymous]
}

function format_users(users, num_anonymous) {
	var content = '<ul style="list-style:none">';
	content = content+'<li style="display:inline;color:grey">Online:</li>';
	if (debug === true) {console.log(getClockTime(true)+" USERS: "+users)};
	if (users.length > 0) {
		var numtabs = {};
		for (var i = 0; i < users.length; i++) {
			var user = users[i];
			if ( numtabs.hasOwnProperty(user) === false) {
				numtabs[user] = 1;
			}
			else {
				numtabs[user] = numtabs[user]+1;
			}
		};
		//console.log("TAB: "+JSON.stringify(numtabs));
		var keys = Object.keys(numtabs);
		keys.sort();
		for (var i=0; i<keys.length; i++) {
		    var user = keys[i];
			var numhtml = "";
			{% if user.is_superuser %}
			{# Displays the number of opened tabs in the broswer #}
			if ( numtabs[user] > 1) {
				numhtml = ' <span style="color:grey;font-size:85%">('+numtabs[user]+')</span>';
			}
			{% endif %}
			content = content+'<li style="display:inline;padding:0 0.5em 0 0.5em">';
			content = content+'<i class="fa fa-user" style="color:lightgrey"></i> '+user;
			content = content+numhtml+'</li>';
		}
	}
	var num_anonymous_ = parseFloat(num_anonymous);
	if ( num_anonymous > 0) {
		if (debug === true) {console.log(num_anonymous_+" anonymous")};
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