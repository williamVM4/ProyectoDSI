const formulario = document.getElementById('agregarpropietario');
const inputs = document.querySelectorAll('#agregarpropietario input');

const expresiones = {
	id:/^[0-9]{8}[ -][0-9]{1}$/,
	nombre:/^([A-ZÀ-ÿ]{1}[A-Za-zÀ-ÿ]+[\s]?)+$/,
	vivienda:/^[A-Za-zÀ-ÿ0-9]{1}([A-Za-zÀ-ÿ]*[\d]*[\W]*[\s]?)+$/,
	profe:/^([A-Za-zÀ-ÿ]+[\s]?)+$/,
	traba:/^([A-Za-zÀ-ÿ]+[\s]?)*$/,
	dirTrabajo:/^([A-Za-zÀ-ÿ0-9]*[\d]*[\W]*[\s]?)*$/,
	telefono2:/^([0-9]{4}[ -][0-9]{4})?$/,
	telefono:/^[0-9]{4}[ -][0-9]{4}$/,
	correo:/^([a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2, 4}$)?/,
}

const campos = {
	dui:false,
	nombrePropietario:false,
	direccion:false,
	profesion:false,
	trabajo:false,
	direccionTrabajo:false,
	telefonoTrabajo:false,
	telefonoCasa:false,
	telefonoCelular:false,
	correoElectronico:false
}

/*FORMULARIO DE AGREGAR PROPIETARIO*/
const validarFormulario = (e) => {
	switch (e.target.name) {
		case "dui": validarCampo(expresiones.id, e.target, 'dui'); break;
		case "nombrePropietario": validarCampo(expresiones.nombre, e.target, 'nombrePropietario');  break;
		case "direccion": validarCampo(expresiones.vivienda, e.target, 'direccion'); break;
		case "profesion": validarCampo(expresiones.profe, e.target, 'profesion');  break;
		case "trabajo": validarCampo(expresiones.traba, e.target, 'trabajo'); break;
		case "direccionTrabajo": validarCampo(expresiones.dirTrabajo, e.target, 'direccionTrabajo');  break;
		case "telefonoTrabajo": validarCampo(expresiones.telefono2, e.target, 'telefonoTrabajo'); break;
		case "telefonoCasa": validarCampo(expresiones.telefono2, e.target, 'telefonoCasa');  break;
		case "telefonoCelular": validarCampo(expresiones.telefono, e.target, 'telefonoCelular');  break;
		case "correoElectronico": validarCampo(expresiones.correo, e.target, 'correoElectronico');  break;
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
	if(campos.nombrePropietario && campos.direccion && campos.profesion && campos.telefonoCelular){
		$('form').submit(function(e){
			$('form').unbind('submit').submit()
		});
	}else{
		e.preventDefault();
		document.getElementById('formulario__mensaje').classList.add('formulario__mensaje-activo');
	}
});




