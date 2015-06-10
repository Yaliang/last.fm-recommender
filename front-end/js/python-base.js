artistFolder = {
	init: function() {
		// initialize the artistFolder 
		this.list = {};
		this.map = {};
		this.maxID = 18745;
		this.requestQueue = [];
		if (typeof(this.interval) != "undefined") {
			clearInterval(this.interval)
		};
		this.interval = window.setInterval(this.refreshFunc , 200, this);
		this.fillQueue = [1,2,3,4];
		this.addNewRandom(4)
	},
	refreshFunc: function(self) {
		// define a refreshing function, which recalled by this.interval and refresh the structure info on artistFolder
		for (var i = 0; i < self.requestQueue.length; i++){
			var ele = self.requestQueue[i]
			var artistID = ele['artistID']
			// console.log(artistID)
			var req = ele['req']
			// console.log(req)
			var method = ele['method']
			if (("readyState" in req) && (req.readyState == 4)) {
				var res = JSON.parse(req.responseText)
				if (method == 'askName'){
					self.list[artistID] = {}
					if ('name' in res) {
						self.list[artistID]['name'] = res.name
						self.list[artistID]['id'] = artistID
						self.queryLastFMInfo(artistID)
					} else {
						// if the asked artist ID has error info
						self.list[artistID]['error'] = res['error']
						self.addNewRandom()
					}
					self.requestQueue.splice(i,1)
				} else if (method == 'askLastFMInfo') {
					self.list[artistID]['lastFM'] = res.artist
					if (self.fillQueue.length > 0) {
						replaceEleID = self.fillQueue.pop();
						if (replaceEleID == 0) {
							if (artistID == self.map[0]) {
								// build a request to wait the knn result loaded
								var newRequest = {}
								newRequest['method'] = 'loadKNNResult'
								newRequest['req'] = {}
								newRequest['artistID'] = artistID
								newRequest['state'] = 0
								self.requestQueue.push(newRequest)
								self.fillKNNResult(self.list[artistID])
							} else {
								self.fillQueue.push(0)
							}
						} else {
							self.fillStructInfo(replaceEleID, self.list[artistID])
							if (self.fillQueue.length == 0) {
								$("#refresh-artists").children(".glyphicon-refresh").removeClass("icon-refresh-animate")
							}
						}
					}
					self.requestQueue.splice(i,1)
				}
			} else if (method == 'loadKNNResult'){
				// handle the knn result 
				var state = ele['state']
				if (state == 4) {
					$("#knn-progress").hide()
					$("#knn-progress").removeClass('active')
					$("#result-title").show()
					$("#artist-0").show()
					$("#artist-0").children('img').width(200)
					// console.log($(this).width())
					$("#artist-0").children('img').height($("#artist-0").children('img').width())
					self.requestQueue.splice(i,1)
				}
			}
		}
	},
	addNewRandom: function(num) {
		// define a function to pick a random number of artist and parse the corresponding info
		if (typeof(num) == "undefined") {
			num = 1
		}
		var newList = {}
		for (var i = 0; i< num; i++) {
			var gotNew = false
			while (!gotNew) {
				var artistID = Math.floor((Math.random()*this.maxID)+1)
				// console.log(artistID)
				gotNew = true
				if ((artistID in this.list) || (artistID in newList)){
					// the random one has been requested before
					gotNew = false
				} else {
					// add request to queue
					newList[artistID] = 'set'
					this.askArtistName(artistID)
				}
			}
		}
	},
	askArtistName: function(artistID) {
		// define a function to ask python-background server return the artist name for an artistID
		var connect = getArtistByID(artistID)
		var newRequest = {}
		newRequest['artistID'] = artistID
		newRequest['req'] = connect
		newRequest['method'] = 'askName'
		this.requestQueue.push(newRequest)
		// console.log(this)
	},
	queryLastFMInfo: function(artistID) {
		// define a function to ask LAST.FM return the artist info for an artist name
		if ((artistID in this.list) && ('name' in this.list[artistID])) {
			var name = this.list[artistID]['name']
		} else {
			return
		}
		var connect = getArtistFromLastFM(name)
		var newRequest = {}
		newRequest['artistID'] = artistID
		newRequest['req'] = connect
		newRequest['method'] = 'askLastFMInfo'
		this.requestQueue.push(newRequest)
	},
	fillNewArtist: function(replaceEleID) {
		// define a function to add the replaceEleID into filling queue
		var ele = $("#artist-"+replaceEleID.toString())
		ele.children('img').attr('src',defaultArtistImageList[replaceEleID-1])
		ele.children('h4').html("Loading...")
		ele.children('span').html("Loading...")
		this.fillQueue.push(replaceEleID)
		this.addNewRandom()
	},
	fillStructInfo: function(replaceEleID, artistObj) {
		// define a function to fill the artist info on the front-end
		this.map[replaceEleID] = artistObj.id
		var ele = $('#artist-'+replaceEleID.toString())
		var artistImgURL = ""
		if (typeof(artistObj.lastFM.image) != "undefined") {
			var imageLeng = artistObj.lastFM.image.length;
			artistImgURL = artistObj.lastFM.image[imageLeng-1]['#text']
		}
		if (artistImgURL.length > 0) {
			var imgele = ele.children('img')
			imgele.attr('src',artistImgURL)
			imgele.load(function(){
				$(this).width(200)
				// console.log($(this).width())
				$(this).height($(this).width())
			})
		}
		var artistName = artistObj.name
		var nameele = ele.children('h4')
		nameele.html(artistName)
		var artistTags = artistObj.lastFM.tags.tag
		var tagele = ele.children('span')
		tagele.html("")
		if (typeof(artistTags) != "undefined") {
			for (var j = 0; j < artistTags.length; j++) {
				tagele.html(tagele.html()+" #"+artistTags[j].name)
			}
		}
	},
	askKNNResult: function(artistID) {
		// define a function to start asking knn result
		this.map[0] = artistID
		var ele = $("#artist-0")
		ele.children('img').attr('src',defaultArtistImageList[1])
		ele.children('h4').html("Loading...")
		ele.children('span').html("Loading...")
		this.fillQueue = [0]
		this.requestQueue = []
		this.askArtistName(artistID)
	},
	fillKNNResult: function(artistObj) {
		// define a function to display the knn result
		var ele = $('#artist-0')
		var imageLeng = artistObj.lastFM.image.length;
		var artistImgURL = artistObj.lastFM.image[imageLeng-1]['#text']
		artistFolder.requestQueue[0]['state'] = 3
		if (artistImgURL.length > 0) {
			var imgele = ele.children('img')
			imgele.attr('src',artistImgURL)
			imgele.load(function(){
				artistFolder.requestQueue[0]['state'] = 4
			})
		}
		var artistName = artistObj.name
		var nameele = ele.children('h4')
		nameele.html(artistName)
		var artistTags = artistObj.lastFM.tags.tag
		var tagele = ele.children('span')
		tagele.html("")
		if (typeof(artistTags) != "undefined") {
			for (var j = 0; j < artistTags.length; j++) {
				tagele.html(tagele.html()+" #"+artistTags[j].name)
			}
		}

	}
}

mockUser = {
	init: function() {
		this.artists = {}
		this.request = []
		this.interval = window.setInterval(this.refreshFunc , 200, this);
	},
	refreshFunc: function(self) {
		for (var i = 0; i < self.request.length; i++){
			var ele = self.request[i]
			var req = ele['connect']
			if (("readyState" in req) && (req.readyState == 4)) {
				var res = JSON.parse(req.responseText)
				var artistID = res['artistID']
				artistFolder.askKNNResult(artistID)
				self.fillAnalytTables(res)
				ele = self.request.pop()
				$("#knn-progress").children(".progress-bar").css('width',"100%").attr('aria-valuenow', "100")
				$("#knn-progress").children(".progress-bar").children(".sr-only").html("100% Complete")
			} else {
				// update the progress bar animation
				var timer = ele['timer']
				timer += 1
				ele['timer'] = timer
				var timerval = Math.round(parseFloat(timer+1) * 0.2 / 3.5 * 100)
				timerval = Math.min(90, timerval)
				$("#knn-progress").children(".progress-bar").css('width',timerval.toString()+"%").attr('aria-valuenow', timerval.toString())
				$("#knn-progress").children(".progress-bar").children(".sr-only").html(timerval.toString()+"% Complete")
			}
		}
	},
	addArtist: function(eleID) {
		var artistID = artistFolder.map[eleID]
		if (!(artistID in this.artists)) {
			this.artists[artistID] = {}
			this.artists[artistID]['weight'] = 1
			this.fillTableRecord(artistID)
			if (eleID != 0) {
				artistFolder.fillNewArtist(eleID)
			} else {
				mockUser.hideResult()
			}
		}
		$('#run-knn').popover('destroy')

	},
	removeArtist: function(artistID) {
		$("#"+artistID.toString()+"tr").animate({
			width:["toggle", "swing"],
			height: ["toggle", "swing"],
			opacity: "toggle"
		}, 300)
		$("#"+artistID.toString()+"tr").remove()
		delete this.artists[artistID]
	},
	fillTableRecord: function(artistID) {
		var artistObj = artistFolder.list[artistID]
		var artistName = artistObj.name
		var artistTags = artistObj.lastFM.tags.tag
		var tag = ""
		if (typeof(artistTags) != "undefined") {
			tag = "#"+artistTags[0].name
		}
		var newSlider = "<input id='"+artistID.toString()+"' data-slider-id='"+artistID.toString()+"Slider' type='text' data-slider-min='0' data-slider-max='1' data-slider-step='0.01' data-slider-tooltip='hide' data-slider-value='"+this.artists[artistID]['weight'].toString()+"'/>"
		var removeBtn = "<button type='button' class='btn btn-default btn-xs' aria-label='remove artist' onclick='mockUser.removeArtist("+artistID.toString()+")'><span class='glyphicon glyphicon-remove-circle' aria-hidden='true'></span>"
		var newTab = "<tr id='"+artistID.toString()+"tr'><td>"+artistID.toString()+"</td><td>"+artistName+"</td><td>"+tag+"</td><td>"+newSlider+"</td><td>"+removeBtn+"</td></tr>"
		var mockTable = $("#mock-user-table").children("tbody")
		mockTable.prepend(newTab)
		var artistSlider = $('#'+artistID.toString()).slider();
		$('#'+artistID.toString()).on("slide", {"artistID": artistID}, function(slideEvt) {
			var artistID = slideEvt.data.artistID
			mockUser.artists[artistID]['weight'] = slideEvt.value
		})
		this.artists[artistID]['slider'] = artistSlider
	},
	fillAnalytTables: function(res) {
		// console.log(res)
		var tagList = res['tags']
		// console.log(tagList)
		var artistsList = res['artists']
		$("#mock-user-features").children("tbody").html("")
		for (var i=0; i<tagList.length; i++) {
			var tagobj = tagList[i]
			var tagID = tagobj['id']
			var tagName = tagobj['name']
			var tagWeight = tagobj['match']
			var newTab = "<tr><td>"+tagID.toString()+"</td><td>"+tagName.toString()+"</td><td>"+tagWeight.toString()+"</td>"
			$("#mock-user-features").children("tbody").append(newTab)
		}
		$("#mock-user-rank").children("tbody").html("")
		for (var i=0; i<artistsList.length; i++) {
			var artistObj = artistsList[i]
			var artistID = artistObj['id']
			var artistName = artistObj['name']
			var artistWeight = artistObj['match']
			var newTab = "<tr><td>"+artistID.toString()+"</td><td>"+artistName.toString()+"</td><td>"+artistWeight.toString()+"</td>"
			$("#mock-user-rank").children("tbody").append(newTab)
		}
	},
	runKNN: function() {
		var url = "http://python-base.herokuapp.com/mockUserWithArtist/";
		var artists = []
		var artistList = Object.keys(this.artists)
		// console.log(artistList)
		var artistLen = artistList.length
		if (artistLen == 0) {
			$('#run-knn').popover('destroy')
			$('#run-knn').popover({
				title: "Message", 
				content: "Please add at least one artist to listen record.",
				trigger: "hover",
			}); 
			$('#run-knn').popover('show')
			return
		}
		this.resultLoading()
		for (var i=0; i<artistLen; i++ ) {
			artistID = artistList[i]
			console.log(artistID)
			listenTime = this.artists[artistID]['weight']
			newRecord = {}
			newRecord[artistID] = listenTime

			artists.push(newRecord)
		}
		artists = JSON.stringify(artists)
		console.log(artists)
		var data = {'artists':artists};
		var connect = $.post(url, data, function(ret){
			// console.log(ret);
		}, "json");
		var newRequest = {}
		newRequest['connect'] = connect
		newRequest['timer'] = 0
		this.request.push(newRequest)
	},
	resultLoading: function() {
		for (var i=1; i<=4; i++) {
			$("#artist-"+i.toString()).animate({
				width:["toggle", "swing"],
				height: ["toggle", "swing"],
				opacity: "toggle"
			}, 300)
		}
		$("#knn-progress").children(".progress-bar").css('width',"10%").attr('aria-valuenow', "10")
		$("#knn-progress").children(".progress-bar").children(".sr-only").html("10% Complete")
		$("#knn-progress").show()
		$("#knn-progress").addClass('active')
		$("#refresh-artists").hide()
		$("#run-knn").hide()
		$("#back-building").show()

	},
	hideResult: function() {
		var imgele;
		for (var i=1; i<=4; i++) {
			$("#artist-"+i.toString()).animate({
				width:["toggle", "swing"],
				height: ["toggle", "swing"],
				opacity: "toggle"
			}, 300, function() {
				imgele = $(this).children('img')
				console.log(this)
				imgele.width(200)
				// console.log($(this).width())
				imgele.height(imgele.width())
			})
			

		}
		$("#artist-0").animate({
			width:["toggle", "swing"],
			height: ["toggle", "swing"],
			opacity: "toggle"
		}, 300)
		$("#refresh-artists").show()
		$("#run-knn").show()
		$("#back-building").hide()
		$("#result-title").hide()
	}
}

defaultArtistImageList = ['data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9InllcyI/PjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIHByZXNlcnZlQXNwZWN0UmF0aW89Im5vbmUiPjxkZWZzLz48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iIzBEOEZEQiIvPjxnPjx0ZXh0IHg9Ijc1LjUiIHk9IjEwMCIgc3R5bGU9ImZpbGw6I0ZGRkZGRjtmb250LXdlaWdodDpib2xkO2ZvbnQtZmFtaWx5OkFyaWFsLCBIZWx2ZXRpY2EsIE9wZW4gU2Fucywgc2Fucy1zZXJpZiwgbW9ub3NwYWNlO2ZvbnQtc2l6ZToxMHB0O2RvbWluYW50LWJhc2VsaW5lOmNlbnRyYWwiPjIwMHgyMDA8L3RleHQ+PC9nPjwvc3ZnPg==', 
	'data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9InllcyI/PjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIHByZXNlcnZlQXNwZWN0UmF0aW89Im5vbmUiPjxkZWZzLz48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iIzM5REJBQyIvPjxnPjx0ZXh0IHg9Ijc1LjUiIHk9IjEwMCIgc3R5bGU9ImZpbGw6IzFFMjkyQztmb250LXdlaWdodDpib2xkO2ZvbnQtZmFtaWx5OkFyaWFsLCBIZWx2ZXRpY2EsIE9wZW4gU2Fucywgc2Fucy1zZXJpZiwgbW9ub3NwYWNlO2ZvbnQtc2l6ZToxMHB0O2RvbWluYW50LWJhc2VsaW5lOmNlbnRyYWwiPjIwMHgyMDA8L3RleHQ+PC9nPjwvc3ZnPg==',
	'data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9InllcyI/PjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIHByZXNlcnZlQXNwZWN0UmF0aW89Im5vbmUiPjxkZWZzLz48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iIzBEOEZEQiIvPjxnPjx0ZXh0IHg9Ijc1LjUiIHk9IjEwMCIgc3R5bGU9ImZpbGw6I0ZGRkZGRjtmb250LXdlaWdodDpib2xkO2ZvbnQtZmFtaWx5OkFyaWFsLCBIZWx2ZXRpY2EsIE9wZW4gU2Fucywgc2Fucy1zZXJpZiwgbW9ub3NwYWNlO2ZvbnQtc2l6ZToxMHB0O2RvbWluYW50LWJhc2VsaW5lOmNlbnRyYWwiPjIwMHgyMDA8L3RleHQ+PC9nPjwvc3ZnPg==',
	'data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9InllcyI/PjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIHByZXNlcnZlQXNwZWN0UmF0aW89Im5vbmUiPjxkZWZzLz48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iIzM5REJBQyIvPjxnPjx0ZXh0IHg9Ijc1LjUiIHk9IjEwMCIgc3R5bGU9ImZpbGw6IzFFMjkyQztmb250LXdlaWdodDpib2xkO2ZvbnQtZmFtaWx5OkFyaWFsLCBIZWx2ZXRpY2EsIE9wZW4gU2Fucywgc2Fucy1zZXJpZiwgbW9ub3NwYWNlO2ZvbnQtc2l6ZToxMHB0O2RvbWluYW50LWJhc2VsaW5lOmNlbnRyYWwiPjIwMHgyMDA8L3RleHQ+PC9nPjwvc3ZnPg==']

function getArtistByID(id) {
	var url = "http://python-base.herokuapp.com/getArtist/"+id.toString();
	var connectToDataset = $.get(url, function(data) {
		// object = JSON.parse(data);
		// console.log(object.name);
		// getArtistFromLastFM(object.name);
	})

	return connectToDataset
}

function getArtistFromLastFM(name) {
	var url = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist="+name+"&api_key=01966bc783793c8d9fede104bdaeff31&format=json";
	// console.log(url);
	var globalGetUrl = $.get(url, function(data) {
		// imageLeng = data.artist.image.length;
		// console.log(data.artist.image[imageLeng-1]['#text']);
		// imageURL = data.artist.image[imageLeng-1]['#text']
	})
	return globalGetUrl
}

function testMockUser() {
	var url = "http://python-base.herokuapp.com/mockUserWithArtist/";
	var artists = []
	var artistLen = 100
	for (i=0; i<artistLen; i++ ) {
		artistID = Math.floor((Math.random()*18745)+1)
		listenTime = Math.floor((Math.random()*artistID)+1)
		newRecord = {}
		newRecord[artistID] = listenTime
		artists.push(newRecord)
	}
	var artists = JSON.stringify(artists)
	var data = {'artists':artists};
	$.post(url, data, function(ret){
		console.log(ret);
	}, "json");

}

function refreshDashBoardArtists() {
	$("#refresh-artists").children(".glyphicon-refresh").addClass("icon-refresh-animate")
	artistFolder.fillQueue = []
	artistFolder.requestQueue = []
	for (var i=1; i<=4; i++) {
		artistFolder.fillNewArtist(i)
	}
}

function displayHelper() {
	$('#run-knn').popover({
		container: 'body',
		title: "Step 4", 
		content: "Execute k nearest neighbor algorithm.",
		trigger: "hover",
		placement: "left"
	}); 
	$('#run-knn').popover('show')
	$('#refresh-artists').popover({
		container: 'body',
		title: "Step 1", 
		content: "Randomly refresh the artists display bellow.",
		trigger: "hover",
		placement: "bottom"
	}); 
	$('#refresh-artists').popover('show')
	$('#add-artist-btn').popover({
		container: 'body',
		title: "Step 2", 
		content: "Add this artist to mock user listen record.",
		trigger: "hover",
		placement: "left"
	}); 
	$('#add-artist-btn').popover('show')
	$('#hide-artist-btn').popover({
		container: 'body',
		title: "Step 2", 
		content: "Load a new artist.",
		trigger: "hover",
		placement: "bottom"
	}); 
	$('#hide-artist-btn').popover('show')

	var newSlider = "<input id='art-1' data-slider-id='art-1-Slider' type='text' data-slider-min='0' data-slider-max='1' data-slider-step='0.01' data-slider-tooltip='hide' data-slider-value='0.8'/>"
	var removeBtn = "<button type='button' class='btn btn-default btn-xs' id='remove-art-btn' aria-label='remove artist' onclick='$(\"#art-1-tr\").remove'><span class='glyphicon glyphicon-remove-circle' aria-hidden='true'></span>"
	var newTab = "<tr id='art-1-tr'><td>-1</td><td>Taylor Swift</td><td>#pop</td><td>"+newSlider+"</td><td>"+removeBtn+"</td></tr>"
	var mockTable = $("#mock-user-table").children("tbody")
	mockTable.prepend(newTab)
	$('#art-1').slider();

	$('#art-1-Slider').popover({
		container: 'body',
		title: "Step 3", 
		content: "Adjust listen record weight.",
		trigger: "hover",
		placement: "bottom"
	}); 
	$('#art-1-Slider').popover('show')

	$('#remove-art-btn').popover({
		container: 'body',
		title: "Step 3", 
		content: "Remove this artist.",
		trigger: "hover",
		placement: "top"
	}); 
	$('#remove-art-btn').popover('show')

	setTimeout(function(){
		$('#run-knn').popover('destroy')
		$('#refresh-artists').popover('destroy')
		$('#add-artist-btn').popover('destroy')
		$('#hide-artist-btn').popover('destroy')
		$('#art-1-Slider').popover('destroy')
		$('#remove-art-btn').popover('destroy')
		$('#art-1-tr').remove()
	}, 5000)
}

function displayBuildUser() {
	$('#build-btn').addClass('active')
	$('#ana-btn').removeClass('active')
}

function displayKNNAna() {
	$('#build-btn').removeClass('active')
	$('#ana-btn').addClass('active')
	var toTop = $('#data-anay').position().top
	$('body').animate({
		scrollTop: toTop
	},"slow")
}

artistFolder.init()
mockUser.init()