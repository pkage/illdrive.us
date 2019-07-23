
const computeCapacities = () => {
    for (let el of document.querySelectorAll('.cars__cardrop')) {
        if (el.childElementCount >= el.dataset.capacity) {
            el.parentElement.setAttribute('data-full', true)
        } else {
            el.parentElement.setAttribute('data-full', false)
        }
    }
}

window.onload = () => {
    dragula([...document.querySelectorAll('[data-drop]')], {
        revertOnSpill: true,
        accepts: (el, target, source, sibling) => {
            return true
        }
    })
    .on('drag', (el) => {
        computeCapacities();

        if (el.parentElement.parentElement.classList.contains('cars__dropcontainer')) {
            // hack, but keeps the .cars__carfull from showing on the dragstart
            el.parentElement.parentElement.setAttribute('data-full', false)
        }
        document.querySelector('.cars').setAttribute('data-dropshown', true)
    })
    .on('dragend', el => {
        document.querySelector('.cars').setAttribute('data-dropshown', false)
    })
}
