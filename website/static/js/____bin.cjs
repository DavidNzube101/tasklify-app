navigationRoute = {
	"Next 1": [signupScreens["1"][0], document.querySelector("#button-next-1"), signupScreens["2"][0], 1, 2],
	"Next 2": [signupScreens["2"][0], document.querySelector("#button-next-2"), signupScreens["3"][0], 2, 3],
	"Prev 2": [signupScreens["2"][0], document.querySelector("#button-prev-2"), signupScreens["1"][0], 2, 1],
	"Prev 3": [signupScreens["3"][0], document.querySelector("#button-prev-3"), signupScreens["2"][0], 3, 2]
} // Defines navigation routes from SCREEN X using BUTTON A to SCREEN Y. Example:- "Next 1": [SCREEN X, BUTTON A, SCREEN Y, X, Y]

// for (navigationRouteProperty in navigationRoute) {
// 	navigationRoute[navigationRouteProperty][1].setAttribute('onclick', `goToNextScreen(signupScreens['${newScreenID}'])`)
// }