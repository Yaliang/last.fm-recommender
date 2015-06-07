artistFolder = {
	init: function() {
		this.list = {};
		this.maxID = 18745;
		this.requestQueue = {};
		if (typeof(this.interval) != "undefined") {
			clearInterval(this.interval)
		};
		this.interval = window.setInterval(this.refreshFunc , 200, this);
	},
	refreshFunc: function(self) {
		keys = Object.keys(self.requestQueue)
		// console.log(this)
		for (i = 0; i < keys.length; i++){
			key = keys[i]
			ele = self.requestQueue[key]
			artistID = ele['artistID']
			console.log(artistID)
			req = ele['req']
			console.log(req)
			method = ele['method']
			if (("readyState" in req) && (req.readyState == 4)) {
				res = JSON.parse(req.responseText)
				if (method == 'askName'){
					self.list[artistID] = {}
					if ('name' in res) {
						self.list[artistID]['name'] = res.name
						self.queryLastFMInfo(artistID)
					} else {
						// if the asked artist ID has error info
						self.list[artistID]['error'] = res['error']
					}
					delete self.requestQueue[key]
				} else if (method == 'askLastFMInfo') {
					self.list[artistID]['lastFM'] = res.artist
					delete self.requestQueue[key]
				}
			}
		}
	},
	addNewRandom: function(num) {
		if (typeof(num) == "undefined") {
			num = 1
		}
		newList = []
		for (i = 0; i< num; i++) {
			gotNew = false
			while (!gotNew) {
				artistID = Math.floor((Math.random()*this.maxID)+1)
				console.log(artistID)
				gotNew = true
				if (artistID in this.list) {
					// the random one has been requested before
					gotNew = false
				} else {
					// add request to queue
					newList.push(artistID)
					this.askArtistName(artistID)
				}
			}
		}
	},
	askArtistName: function(artistID) {
		connect = getArtistByID(artistID)
		newRequest = {}
		newRequest['artistID'] = artistID
		newRequest['req'] = connect
		newRequest['method'] = 'askName'
		newKey = Object.keys(this.requestQueue).length
		this.requestQueue[newKey] = newRequest
		console.log(this)
	},
	queryLastFMInfo: function(artistID) {
		if ((artistID in this.list) && ('name' in this.list[artistID])) {
			name = this.list[artistID]['name']
		} else {
			return
		}
		connect = getArtistFromLastFM(name)
		newRequest = {}
		newRequest['artistID'] = artistID
		newRequest['req'] = connect
		newRequest['method'] = 'askLastFMInfo'
		newKey = Object.keys(this.requestQueue).length
		this.requestQueue[newKey] = newRequest
	},
	fillNewArtist:function(replaceEleID) {
		
	}
}

waitQueue = {}
globalInter = window.setInterval(function(){
	keys = Object.keys(waitQueue)
	for (i = 0; i < keys.length; i++){
		key = keys[i]
		ele = waitQueue[key]
		if (("readyState" in ele) && (ele.readyState == 4)) {
			res = ele.responseJSON;
			imagelen = res.artist.image.length;
			imageURL = res.artist.image[imagelen -1]['#text'];
			console.log(imageURL)
			delete waitQueue[key]
		}
	}
}, 300)

function getArtistByID(id) {
	url = "http://python-base.herokuapp.com/getArtist/"+id.toString();
	connectToDataset = $.get(url, function(data) {
		// object = JSON.parse(data);
		// console.log(object.name);
		// getArtistFromLastFM(object.name);
	})

	return connectToDataset
}

function getArtistFromLastFM(name) {
	url = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist="+name+"&api_key=01966bc783793c8d9fede104bdaeff31&format=json";
	console.log(url);
	globalGetUrl = $.get(url, function(data) {
		// imageLeng = data.artist.image.length;
		// console.log(data.artist.image[imageLeng-1]['#text']);
		// imageURL = data.artist.image[imageLeng-1]['#text']
	})
	return globalGetUrl
}

function testMockUser() {
	url = "http://python-base.herokuapp.com/mockUserWithArtist/";
	artists = []
	artistLen = 100
	for (i=0; i<artistLen; i++ ) {
		artistID = Math.floor((Math.random()*18745)+1)
		listenTime = Math.floor((Math.random()*artistID)+1)
		newRecord = {}
		newRecord[artistID] = listenTime
		artists.push(newRecord)
	}
	artists = JSON.stringify(artists)
	data = {'artists':artists};
	$.post(url, data, function(ret){
		console.log(ret);
	}, "json");

}

function refreshDashBoardArtists() {
	for (i=0; i<4; i++) {

	}
}