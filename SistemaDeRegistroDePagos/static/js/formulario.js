const formulario = document.getElementById('AgregarProyectoTuristico');
const inputs = document.querySelectorAll('#AgregarProyectoTuristico input');

const expresiones = {
	nombrePropio: /^([A-ZÀ-ÿ]{1}[A-Za-zÀ-ÿ]+[\s]*)+$/,
}

const campos = {
	//Proyecto turístico
	nombreProyectoTuristico: false,
	empresa:false
}

/*FORMULARIO DE AGREGAR PROYECTO*/
const validarFormulario = (e) => {
	switch (e.target.name) {
		case "nombreProyectoTuristico":
			validarCampo(expresiones.nombrePropio, e.target, 'nombreProyectoTuristico'); //(expresion regular, input,nombre del campo)
		break;
		case "empresa": validarCampo(expresiones.nombrePropio, e.target, 'empresa');  break;
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

//aqui es donde luego de escribir algo "keyup" hacemos que se valide algo
//El blur es para validar si está fuera del campo
inputs.forEach((input) => {
	input.addEventListener('keyup', validarFormulario);
	input.addEventListener('blur', validarFormulario);
});

formulario.addEventListener('submit', (e) => {
	if(campos.nombreProyectoTuristico && campos.empresa){
		$('form').submit(function(e){
			$('form').unbind('submit').submit()
		});
	} else {
		e.preventDefault();
		document.getElementById('formulario__mensaje').classList.add('formulario__mensaje-activo');
	}
});




