console.log(`[INFO]: Loaded page to screen ${current_screen}`)

// ScreenElement, ScreenID 

home_screen = [document.querySelector("#home-screen"), 1]
withdraw_screen = [document.querySelector("#withdraw-screen"), 5]
help_screen = [document.querySelector("#help-screen"), 6]
settings_screen = [document.querySelector("#settings-screen"), 7]

// Triggers
home_trigger = document.querySelector("#home-button")
help_trigger_2 = document.querySelector("#help-button-2")
withdraw_trigger = document.querySelector("#withdraw-button")
withdraw_trigger_2 = document.querySelector("#withdraw-button-2")
help_trigger = document.querySelector("#help-button")
settings_trigger = document.querySelector("#settings-button")

window.addEventListener('load', ()=>{
	// window.location.href = `/dashboard/${current_screen}`
	switch (current_screen) {

		case 5:
			home_screen[0].style.display = 'none'
			withdraw_screen[0].style.display = 'block'
			help_screen[0].style.display = 'none'
			settings_screen[0].style.display = "none"
			current_screen = 5
			break;

		case 6:
			home_screen[0].style.display = 'none'
			withdraw_screen[0].style.display = 'none'
			help_screen[0].style.display = 'block'
			settings_screen[0].style.display = "none"
			current_screen = 6
			break;

		case 7:
			home_screen[0].style.display = 'none'
			withdraw_screen[0].style.display = 'none'
			help_screen[0].style.display = 'none'
			settings_screen[0].style.display = "block"
			current_screen = 7
			break;

		default:
			home_screen[0].style.display = 'block'
			withdraw_screen[0].style.display = 'none'
			help_screen[0].style.display = 'none'
			settings_screen[0].style.display = "none"
	}

})

home_trigger.addEventListener('click', ()=>{
	home_screen[0].style.display = 'block'
	withdraw_screen[0].style.display = 'none'
	help_screen[0].style.display = 'none'
	settings_screen[0].style.display = "none"
	current_screen = 1
})
withdraw_trigger.addEventListener('click', ()=>{
	home_screen[0].style.display = 'none'
	withdraw_screen[0].style.display = 'block'
	help_screen[0].style.display = 'none'
	settings_screen[0].style.display = "none"
	current_screen = 5
})
help_trigger.addEventListener('click', ()=>{
	home_screen[0].style.display = 'none'
	withdraw_screen[0].style.display = 'none'
	help_screen[0].style.display = 'block'
	settings_screen[0].style.display = "none"
	current_screen = 6
})
withdraw_trigger_2.addEventListener('click', ()=>{
	home_screen[0].style.display = 'none'
	withdraw_screen[0].style.display = 'block'
	help_screen[0].style.display = 'none'
	settings_screen[0].style.display = "none"
	current_screen = 5
})
help_trigger_2.addEventListener('click', ()=>{
	home_screen[0].style.display = 'none'
	withdraw_screen[0].style.display = 'none'
	help_screen[0].style.display = 'block'
	settings_screen[0].style.display = "none"
	current_screen = 6
})
settings_trigger.addEventListener('click', ()=>{
	home_screen[0].style.display = 'none'
	withdraw_screen[0].style.display = 'none'
	help_screen[0].style.display = 'none'
	settings_screen[0].style.display = "block"
	current_screen = 7
})