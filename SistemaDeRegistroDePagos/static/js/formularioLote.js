/*FORMULARIO DE AGREGAR LOTE*/
const formulario = document.getElementById('AgregarLote');
const inputs = document.querySelectorAll('#AgregarLote input');
const expresiones = {
	matricula: /^\d{8}/,
	numero:/^\d{1}(\d+)?/,
	pol: /^([A-Z]{1}[a-z]?)/,
	area: /^\d+(.{1}\d{2})?/,
}

const campos = {
	matriculaLote:false,
	numeroLote:false,
	poligono:false,
	areaMCuadrado:false
}

const validarFormulario = (e) => {
	switch (e.target.name) {
		case "matriculaLote": validar(expresiones.matricula, e.target, 'matriculaLote');break;
		case "numeroLote": validar(expresiones.numero, e.target, 'numeroLote'); break;
		case "poligono": validar(expresiones.pol, e.target, 'poligono'); break;
		case "areaMCuadrado": validar(expresiones.area, e.target, 'areaMCuadrado'); break;
	}
}
const validar = (expresion, input, campo) => {
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
	if(campos.matriculaLote && campos.numeroLote && campos.poligono && campos.areaMCuadrado){
		$('form').submit(function(e){
			$('form').unbind('submit').submit()
		});
	} else {
		e.preventDefault();
		document.getElementById('formulario__mensaje').classList.add('formulario__mensaje-activo');
	}
});
