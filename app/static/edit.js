
const computeCapacities = () => {
    console.log('computing capacity')
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
            console.log(target.parentElement.dataset.full)
            return true
        }
    })
    .on('drag', (el) => {
        computeCapacities();
        document.querySelector('.cars').setAttribute('data-dropshown', true)
    })
    .on('dragend', el => {
        document.querySelector('.cars').setAttribute('data-dropshown', false)
    })
}
