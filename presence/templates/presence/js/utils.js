{% load i18n %}

var instantDebug = true;

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
	return [users, anonymous]
}

function format_users(users, num_anonymous) {
	if ( instantDebug === true ) {
		console.log(getClockTime(true)+" Users: "+users+' + '+anonymous+' anonymous')
	};
	var content = '<ul style="list-style:none">';
	content = content+'<li id="presence-title">Online:</li>';
	if (users) {
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
						numhtml = ' <span style="presence-usertabs">('+numtabs[user]+')</span>';
					}
				{% endif %}
				content = content+'<li class="presence-user">';
				content = content+'<i class="fa fa-user" style="color:lightgrey"></i> '+user;
				content = content+numhtml+'</li>';
			}
		}
	}
	var num_anonymous_ = parseFloat(num_anonymous);
	if ( num_anonymous > 0) {
		if ( num_anonymous_ == 1) {
			content = content+'<li class="presence-user"> '+num_anonymous+" {% trans 'anonymous user' %}"+'</li>';
		}
		else {
			content = content+'<li class="presence-user"> '+num_anonymous+" {% trans 'anonymous users' %}"+'</li>';
		}
	}
	content = content+'</ul>';
	return content
}