
//function to check if string only contains white spaces
function isAllBlank(str) {
    if (!str.replace(/\s/g, '').length) {
        /*si al remplazar todos los espacio por un vacio el
         length es 0 es porque todos los caracteres eran espacios */
        return true
    }
    else {
        return false
    }
}

export {isAllBlank}