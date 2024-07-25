function goToRoute(route, method) {
	if (method[0] == 'GET') {
		window.location.pathname = route
	} else {
		var data = method[1]
		const url = `${window.location}${route}`
		fetch(url, {
			method: 'POST',
			headers: {'Content-Type': 'application/json'},
			body: JSON.stringify(data)
		})
		.then(response => response.text())
		.then(data => console.log(data))
	}
}

// Sign Up Screens Logic

try {
	signupScreens = {
		"1": [document.querySelector("#sg-screen-1"), 1],
		"2": [document.querySelector("#sg-screen-2"), 2],
		"3": [document.querySelector("#sg-screen-3"), 3]
	}

	function exceptDisplayStyle(screenObject, displayProperty) {
		try{
			screenObject.style.display = displayProperty
		} catch (error) {
			console.log(error)
		}
	}

	function hideScreens(exceptionScreenObject) {
		for (screenObject in signupScreens) {
			console.log(`Hiding\n\nID: ${signupScreens[screenObject][0]}\nELEMENT: ${signupScreens[screenObject][1]}`)
			signupScreens[screenObject][0].style.display = "none"
		}
		if (exceptionScreenObject == "NULL") {
			console.log("No screen passed for hiding exception")
		} else {
			console.log(`Hiding Exception: ${exceptionScreenObject}`)
			exceptDisplayStyle(exceptionScreenObject, "block")
		}
	}

	function showScreens(exceptionScreenObject) {
		for (screenObject in signupScreens) {
			console.log(`Showing\n\nID: ${signupScreens[screenObject][0]}\nELEMENT: ${signupScreens[screenObject][1]}`)
			signupScreens[screenObject][0].style.display = "block"
		}
		if (exceptionScreenObject == "NULL") {
			console.log("No screen passed for showing exception")
		} else {
			exceptDisplayStyle(exceptionScreenObject, "none")
		}
	}

	function goToNextScreen(screenData) {
		currentScreen = `${screenData[0]}`
		currentScreenID = screenData[1]

		newScreenID = currentScreenID + 1
		newScreen = `#sg-screen-${currentScreen.replace(`${currentScreenID}`, `${newScreenID}`)}`

		hideScreens(document.querySelector(`#sg-screen-${newScreenID}`))
		
		console.log(`Current Screen: ${currentScreen}\nCurrent Screen ID: ${currentScreenID}\n\nNext Screen: ${newScreen}\nNext Screen ID: ${currentScreenID + 1}`)
	}

	function goToPrevScreen(screenData) {
		currentScreen = `${screenData[0]}`
		currentScreenID = screenData[1]

		newScreenID = currentScreenID - 1
		newScreen = `#sg-screen-${currentScreen.replace(`${currentScreenID}`, `${newScreenID}`)}`
		
		hideScreens(document.querySelector(`#sg-screen-${newScreenID}`))


		console.log(`Current Screen: ${currentScreen}\nCurrent Screen ID: ${currentScreenID}\n\nPrevious Screen: ${newScreen}\nPrevious Screen ID: ${currentScreenID - 1}`)
	}



	try{
		hideScreens(signupScreens[`${defaultSignupScreen}`][0])
	} catch (error) {
		hideScreens(signupScreens["1"][0])
	}

} catch (error) {
	console.log(`Error: ${error}\nMeaning: Sign Up Logic can't work outside onboaring.html`)
}

try {
	// hides labels/flashes after 5 seconds
	const labels = document.querySelectorAll(".inforamtion-label")
	labels.forEach(label => {
		setTimeout(()=>{
			label.style.display = "none"
		}, 5000)
	})
} catch (error) {
	console.log(error)
}

try {
	const form = document.querySelector("#withdraw-screen")

	function updateStatusText(element, _display, text) {
		element.style.display = _display
		element.innerHTML = text
		setTimeout(()=>{
			element.style.display = "none"
		}, 5000)
	}

	form.addEventListener('submit', (e) => {
		e.preventDefault();

		const accountNumber = document.querySelector("#account_number").value
		const bankName = document.querySelector("#bank").value
		const availableBalance = document.querySelector("#available_balance").value
		const amountToWithdraw = document.querySelector("#amount").value
		let status = document.querySelector("#status_text_wth")

		if (accountNumber.length < 10) {
			updateStatusText(status, "block", 'Account Number Less than 10 digits')
			return;
		}
		if (accountNumber.length > 10) {
			updateStatusText(status, "block", 'Account Number More than 10 digits')
			return;
		}
		if (bankName == "None" || bankName == "Select Destination Bank") {
			updateStatusText(status, "block", 'Select a bank')
			return;
		}
		// if (walletPassword !== password) {
		// 	updateStatusText(status, "block", 'Password Incorrect')
		// 	return;
		// }
		if (amountToWithdraw == "" || amountToWithdraw == "0") {
			updateStatusText(status, "block", "Can't withdraw TT 0")
			return;
		}
		if (parseInt(amountToWithdraw) > parseInt(availableBalance)) {
			updateStatusText(status, "block", 'Insufficient Funds')
			return;
		}

		form.submit();
	})
} catch (error) {
	console.log(error)
}