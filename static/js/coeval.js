function jumpTo(anchor) {
	document.getElementById(anchor).scrollIntoView();
}

/* Home page */

function addCoev() {
    document.getElementById("add-coev-form").style.display = "block";
    document.getElementById("add-curso-form").style.display = "none";
    document.getElementById("add-coev-btn").classList.add("active");
    document.getElementById("add-curso-btn").classList.remove("active");
}

function addCurso() {
    document.getElementById("add-coev-form").style.display = "none";
    document.getElementById("add-curso-form").style.display = "block";
    document.getElementById("add-coev-btn").classList.remove("active");
    document.getElementById("add-curso-btn").classList.add("active");
}

function cancelAdd() {
    document.getElementById("add-coev-form").style.display = "none";
    document.getElementById("add-curso-form").style.display = "none";
    document.getElementById("add-coev-btn").classList.remove("active");
    document.getElementById("add-curso-btn").classList.remove("active");
}

/* Perfil */

function checkPass()
{
    var pass1 = document.getElementById('passNew');
    var pass2 = document.getElementById('passNewConfirm');
    var goodColor = "#66cc66";
    var badColor = "#ff6666";
    var white = "#ffffff";
    if(pass1.value === pass2.value){
        pass2.style.backgroundColor = goodColor;
    }else if(pass2.value === ""){
        pass2.style.backgroundColor = white;
    }else{
        pass2.style.backgroundColor = badColor;
    }
}

function changePass() {
    document.getElementById("cambiar-contrasena").style.display = "block";
    document.getElementById("notas-resumen").style.display = "none";
    document.getElementById("notas-placeholder").style.display = "none";
    var active = document.getElementsByClassName("active");
    if(active.length>=1){
        active[0].classList.remove("active");
    }
    document.getElementById("change-pass-btn").classList.add("active");
}

function loadCurso(id_curso) {
    cursocodigo = document.getElementById("cursocodigo"+id_curso).textContent;
    cursoano = document.getElementById("cursoano"+id_curso).textContent;
    return cursocodigo+', '+cursoano;
}

function showNotas(id_curso, n_cursos, n_coev) {
    document.getElementById("currentCurso").innerHTML = loadCurso(id_curso);
    document.getElementById("cambiar-contrasena").style.display = "none";
    document.getElementById("notas-resumen").style.display = "block";
    document.getElementById("notas-placeholder").style.display = "none";

    var active = document.getElementsByClassName("active");
    if(active.length>=1){
        active[0].classList.remove("active");
    }
    for(i = 0; i<= n_cursos; i++){

        for(j = 0; j<=n_coev; j++){
            idval=i+"-"+j;
            if (i === id_curso) {
                try{
                    document.getElementById(idval).style.display = "table-row";
                }catch{}
            } else {
                try {
                    document.getElementById(idval).style.display = "none";

                } catch {
                }
            }
        }
    }
    document.getElementById("row-btn"+id_curso).classList.add("active");

}


function cancelPass() {
    document.getElementById("cambiar-contrasena").style.display = "none";
    document.getElementById("notas-resumen").style.display = "none";
    document.getElementById("change-pass-btn").classList.add("active");
    document.getElementById("notas-placeholder").style.display = "block";
}

/* Gestión Curso */

function showGestionEstudiante() {
    document.getElementById("gestion-grupo").style.display = "none";
    document.getElementById("gestion-estudiante").style.display = "block";
    document.getElementById("gestion-placeholder").style.display = "none";
    document.getElementById("active-estudiante").classList.add("active");
    document.getElementById("active-grupo").classList.remove("active");
}

function showGestionGrupo() {
    document.getElementById("gestion-grupo").style.display = "block";
    document.getElementById("gestion-estudiante").style.display = "none";
    document.getElementById("gestion-placeholder").style.display = "none";
    document.getElementById("active-grupo").classList.add("active");
    document.getElementById("active-estudiante").classList.remove("active");
}