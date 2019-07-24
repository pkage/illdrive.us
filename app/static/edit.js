const computeCapacities = () => {
    for (let el of document.querySelectorAll('.cars__cardrop')) {
        if (el.childElementCount >= el.dataset.capacity) {
            // hack!
            el.parentElement.setAttribute('data-full', true)
            el.parentElement.parentElement.setAttribute('data-full', true)
        } else {
            // also a hack
            el.parentElement.setAttribute('data-full', false)
            el.parentElement.parentElement.setAttribute('data-full', false)
        }
    }
}

document.querySelector('#addcar').addEventListener('click', e => {
    let el = document.querySelector('#addcar')

    if (!el.classList.contains('cars__addcar--active')) {
        el.classList.add('cars__addcar--active')
        document.querySelector('#addcar__name').focus()
    }
})

document.querySelector('#addcar__name').addEventListener('keyup', e => {
    if (e.key === 'Enter') {
        console.log(e.target.value);
    } else if (e.key === 'Escape') {
        e.target.value = '';
        document.querySelector('#addcar').classList.remove('cars__addcar--active')
    }
})
document.querySelector('#addcar__name').addEventListener('blur', e => {
    e.target.value = '';
    document.querySelector('#addcar').classList.remove('cars__addcar--active')
})

document.querySelectorAll('.cars__cardelete').forEach(el => {
    el.addEventListener('click', e => {
        console.log(`deleting car ${e.target.dataset.id}`)
    })
})


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
            el.parentElement.parentElement.parentElement.setAttribute('data-full', false)
        }
        document.querySelector('.cars').setAttribute('data-dropshown', true)
    })
    .on('dragend', el => {
        document.querySelector('.cars').setAttribute('data-dropshown', false)
    })
}

