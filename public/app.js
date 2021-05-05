var fighters = null;
var fighter_id = null;

function deleteFighterOnServer(FighterId) {
	fetch("http://localhost:8080/fighters/" + FighterId, {
		method: "DELETE",
		credentials: "include"
	}).then(function (response) {
		loadFighters();
	});
}

//views
var userView = document.querySelector("#userView");
var dash = document.querySelector("#dash");


//register

var user_first_name = document.querySelector("#first-name");
var user_last_name = document.querySelector("#last-name");
var user_email = document.querySelector("#email");
var user_password = document.querySelector("#password");
var register_button = document.querySelector("#register-button");

//login

var username = document.querySelector("#username");
var passw = document.querySelector("#passw");
var login_button = document.querySelector('#login-button');

// Auth

register_button.onclick = function() {
	var first_name = user_first_name.value;
	var last_name = user_last_name.value;
    var email = user_email.value;
	var pass = user_password.value;

	var data = 'first_name=' + encodeURIComponent(first_name);
    data += '&last_name=' + encodeURIComponent(last_name);
    data += '&email=' + encodeURIComponent(email);
    data += '&password=' + encodeURIComponent(pass);
	
	fetch("http://localhost:8080/users", {
		method: "POST",
		credentials: "include",
		body: data,
		headers: {
			"Content-Type": "application/x-www-form-urlencoded"
		}
	}).then(function(response) {
		if (response.status == 201) {
			var success = document.createElement("p");
			success.innerHTML = "Registration complete";
			document.querySelector("#register").appendChild(success);
		} else {
			alert("This username already exists");
		}

	})
	resetForm([user_first_name, user_last_name, user_email, user_password]);
}

function resetForm(inputs) {
    for (i = 0; i < inputs.length; i++) {
        inputs[i].value = '';
    }

    addButton.classList.remove('hidden');
    updateButton.classList.add('hidden');
}

login_button.onclick = function() {
    var u_name = username.value;
    var pass = passw.value;

    var data = 'email=' + encodeURIComponent(u_name);
    data += '&password=' + encodeURIComponent(pass);

    fetch("http://localhost:8080/sessions", {
        method: "POST",
        credentials: "include",
        body: data,
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    }).then(function(response) {
        console.log(response);
        if (response.status == 201) {
            userView.classList.add("hidden")
            dash.classList.remove('hidden');
            console.log(response);
            displayData();
        } else {
            alert("Your username or password is incorrect! Try again");
            clearInputs([username, passw]);
        }
    })
}

var updateButton = document.querySelector("#update-button");
console.log("the update button", updateButton);

updateButton.onclick = function () {
		var fighterNameInput = document.querySelector("#fighter-name");
		var fighterName = fighterNameInput.value;
		var fighterColorInput = document.querySelector("#fighter-color");
		var fighterColor = fighterColorInput.value;
		var fighterStyleInput = document.querySelector("#fighter-style");
		var fighterStyle = fighterStyleInput.value;
		var fighterStockInput = document.querySelector("#fighter-stock");
		var fighterStock = fighterStockInput.value;
		var fighterHpInput = document.querySelector("#fighter-hp");
		var fighterHp = fighterHpInput.value;
		console.log("You entered:", fighterName);

		var data = "name=" + encodeURIComponent(fighterName);
		data += "&color=" + encodeURIComponent(fighterColor);
		data += "&style=" + encodeURIComponent(fighterStyle);
		data += "&stock=" + encodeURIComponent(fighterStock);
		data += "&hp=" + encodeURIComponent(fighterHp);

		fetch("http://localhost:8080/fighters/" + fighter_id, {
			method: "PUT", 
			credentials: "include",
			body: data,
			headers: {
				"Content-Type": "application/x-www-form-urlencoded"
			}
		}).then(function (response) {
			loadFighters();
		});

		resetForm([fighterNameInput, fighterColorInput, fighterStyleInput, fighterStockInput, fighterHpInput]);
}


var addButton = document.querySelector("#add-button");
console.log("the button", addButton);

addButton.onclick = function () {
		var fighterNameInput = document.querySelector("#fighter-name");
		var fighterName = fighterNameInput.value;
		var fighterColorInput = document.querySelector("#fighter-color");
		var fighterColor = fighterColorInput.value;
		var fighterStyleInput = document.querySelector("#fighter-style");
		var fighterStyle = fighterStyleInput.value;
		var fighterStockInput = document.querySelector("#fighter-stock");
		var fighterStock = fighterStockInput.value;
		var fighterHpInput = document.querySelector("#fighter-hp");
		var fighterHp = fighterHpInput.value;
		console.log("You entered:", fighterName);

		var data = "name=" + encodeURIComponent(fighterName);
		data += "&color=" + encodeURIComponent(fighterColor);
		data += "&style=" + encodeURIComponent(fighterStyle);
		data += "&stock=" + encodeURIComponent(fighterStock);
		data += "&hp=" + encodeURIComponent(fighterHp);

		fetch("http://localhost:8080/fighters", {
			method: "POST",
			credentials: "include", 
			body: data,
			headers: {
				"Content-Type": "application/x-www-form-urlencoded"
			}
		}).then(function (response) {
			loadFighters();
		});
		resetForm([fighterNameInput, fighterColorInput, fighterStyleInput, fighterStockInput, fighterHpInput]);
}



function loadFighters () {
	fetch("http://localhost:8080/fighters", {
		credentials: "include"
	}).then(function (response) {
		response.json().then(function (fightersFromServer) {
			fighters = fightersFromServer;

			var fightersList = document.querySelector("#fighters-list");
			fightersList.innerHTML = "";
			fighters.forEach(function (fighter) {
				console.log("one fighter:", fighter);
				var listItem = document.createElement("li");

				var nameEl = document.createElement("div");
				nameEl.innerHTML = fighter.name;
				nameEl.classList.add("name");
				listItem.appendChild(nameEl);

				var colorEl = document.createElement("div");
				colorEl.innerHTML = fighter.color;
				colorEl.classList.add("color");
				listItem.appendChild(colorEl);

				var styleEl = document.createElement("div");
				styleEl.innerHTML = fighter.style;
				styleEl.classList.add("style");
				listItem.appendChild(styleEl);

				var stockEl = document.createElement("div");
				stockEl.innerHTML = fighter.stock;
				stockEl.classList.add("stock");
				listItem.appendChild(stockEl);

				var hpEl = document.createElement("div");
				hpEl.innerHTML = fighter.hp;
				hpEl.classList.add("hp");
				listItem.appendChild(hpEl);

				var editButton = document.createElement("button");
				editButton.innerHTML = "Edit";
				editButton.onclick = function() {
					fighter_id = fighter.id;

					var fighterNameInput = document.querySelector("#fighter-name");
					var fighterColorInput = document.querySelector("#fighter-color");
					var fighterStyleInput = document.querySelector("#fighter-style");
					var fighterStockInput = document.querySelector("#fighter-stock");
					var fighterHpInput = document.querySelector("#fighter-hp");

					fighterNameInput.value = fighter.name
					fighterColorInput.value = fighter.color
					fighterStyleInput.value = fighter.style
					fighterStockInput.value = fighter.stock
					fighterHpInput.value = fighter.hp
				}
				listItem.appendChild(editButton);

				var deleteButton = document.createElement("button");
				deleteButton.innerHTML = "Delete";
				deleteButton.onclick = function () {
					console.log("you clicked me.", fighter);
					if (confirm("Are you sure your want to delete" + fighter.name + "?")) {
						deleteFighterOnServer(fighter.id)
					}
				};
				listItem.appendChild(deleteButton);

				fightersList.appendChild(listItem);

			});
		});
	});
}



//loadFighters()

function displayDash() {
	userView.classList.add("hidden");
	dash.classList.remove("hidden");

	var name = document.querySelector("#user");
}

function displayData() {
	console.log("called");
	fetch("http://localhost:8080/fighters", {
		credentials: "include"
	}).then(function(response){
		console.log(response);
		if (response.status == 401) {
			console.log("not allowed");
			return;
		} else {
			displayDash();
			loadFighters();
		}
	})
}

displayData();


