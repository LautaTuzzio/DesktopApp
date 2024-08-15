function showSection(sectionId, element) {
    document.querySelectorAll('.content').forEach(section => {
        section.style.display = 'none'
    })

    document.getElementById(sectionId).style.display = 'block'
    
    var options = document.querySelectorAll('.option')
    options.forEach(function(option) {
        option.classList.remove('active')
    })

    element.classList.add('active')
}

document.addEventListener('DOMContentLoaded', function() {
    var defaultOption = document.getElementById('activity-button')
    var defaultSectionId = 'activity' 
    showSection(defaultSectionId, defaultOption)
})
