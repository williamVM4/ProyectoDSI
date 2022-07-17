const formulario = document.getElementById('AgregarDetalleVenta');
const inputs = document.querySelectorAll('#AgregarDetalleVenta input');

const expresiones = {
	flotante: /^\d+(.{1}\d{1,2})?$/,
}

const campos = {
	precioVenta: false,
	descuento:false
}

/*FORMULARIO DE AGREGAR DETALLE DE VENTA*/
const validarFormulario = (e) => {
	switch (e.target.name) {
		case "precioVenta": validarCampo(expresiones.flotante, e.target, 'precioVenta'); break;
		case "descuento": validarCampo(expresiones.flotante, e.target, 'descuento');  break;
	}
}

const validarCampo = (expresion, input, campo) => {
	if(expresion.test(input.value)){
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto');
		document.querySelector(`#grupo__${campo} i`).classList.add('fa-check-circle');
		document.querySelector(`#grupo__${campo} i`).classList.remove('fa-times-circle');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.remove('formulario__input-error-activo');
		campos[campo] = true;
		document.getElementById('formulario__mensaje').classList.remove('formulario__mensaje-activo');
	} else {
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-correcto');
		document.querySelector(`#grupo__${campo} i`).classList.add('fa-times-circle');
		document.querySelector(`#grupo__${campo} i`).classList.remove('fa-check-circle');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.add('formulario__input-error-activo');
		campos[campo] = false;
	}
}

inputs.forEach((input) => {
	input.addEventListener('keyup', validarFormulario);
	input.addEventListener('blur', validarFormulario);
});

formulario.addEventListener('submit', (e) => {
	if(campos.precioVenta && campos.descuento){
		$('form').submit(function(e){
			$('form').unbind('submit').submit()
		});
	} else {
		e.preventDefault();
		document.getElementById('formulario__mensaje').classList.add('formulario__mensaje-activo');
	}
});




